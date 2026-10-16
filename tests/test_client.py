import pytest
from aspire_agent.client import AspenClient,AspenError,is_explicitly_complete
class Response:
    status_code=200
    def __init__(self,body): self.body=body
    def json(self): return self.body
class Transport:
    def __init__(self): self.calls=[]; self.queue=[]; self.timeouts=[]
    def request(self,method,url,*,json=None,timeout=None): self.calls.append((method,url,json)); self.timeouts.append(timeout); return Response(self.queue.pop(0) if self.queue else {"success":True})
def operations(t): return [call[2]["operation"] for call in t.calls if call[1].endswith("/session/execute")]
def test_canonical_session_payloads():
    t=Transport();c=AspenClient("http://x",transport=t);c.start("k");c.start("k",show_gui=False);c.load("k","a.bkp");c.checkpoint("k","c.bkp");c.close("k")
    assert t.calls[0][2]=={"task_hash":"k"};assert t.calls[1][2]["show_gui"] is False;assert t.calls[2][2]["bkp_path"]=="a.bkp";assert t.calls[3][2]["filename"]=="c.bkp";assert t.calls[4][2]=={"task_hash":"k"}
@pytest.mark.parametrize("ports",[{"F(IN)":[]},[{"name":"F(IN)","connected_streams":[]}]])
def test_connect_accepts_canonical_and_local_port_shapes(ports):
    t=Transport();t.queue=[{"success":True,"ports":ports},{"success":True}];AspenClient(transport=t).connect_stream("k","M1","F1","F(IN)");assert operations(t)==["list_block_ports","connect_stream"]
def test_components_use_canonical_two_call_verification():
    t=Transport();t.queue=[{"success":True,"components_added":[{"component_id":"WATER","cas":"7732-18-5"}],"verification":{"success":True}},{"success":True,"rows":[{"component_id":"WATER","cas":"7732-18-5"}],"missing_requested_component_ids":[]}];result=AspenClient(transport=t).add_components("k",["water"])
    assert operations(t)==["add_components_by_cas","inspect_component_table"];assert t.calls[0][2]["parameters"]["components"]==[{"component_id":"WATER","cas":"7732-18-5"}];assert t.calls[1][2]["parameters"]=={"component_ids":["WATER"]};assert result["inspection"]["rows"]
    t=Transport();t.queue=[{"success":False,"components_added":[],"verification":{"success":False}},{"missing_requested_component_ids":["WATER"]}]
    with pytest.raises(AspenError): AspenClient(transport=t).add_components("k",["water"])
def test_mixer_exact_setter_sequence():
    t=Transport();AspenClient(transport=t).configure_mixer("k","M1",energy_balance=True,pressure=2,pressure_unit="bar");assert operations(t)==["set_energy_bal","set_pres"];assert t.calls[0][2]["parameters"]=={"block_name":"M1","value":"YES"};assert t.calls[1][2]["parameters"]=={"block_name":"M1","value":2,"unit":"bar"}
@pytest.mark.parametrize(("mode","values","expected"),[("TP",{"temperature":350,"temperature_unit":"K","pressure":2,"pressure_unit":"bar"},["set_spec_opt","set_temp","set_pres"]),("PV",{"pressure":2,"pressure_unit":"bar","vapor_fraction":.5},["set_spec_opt","set_pres","set_vfrac"]),("PD",{"pressure":2,"pressure_unit":"bar","duty":0,"duty_unit":"kW"},["set_spec_opt","set_pres","set_duty"])])
def test_heater_exact_setter_sequences(mode,values,expected):
    t=Transport();AspenClient(transport=t).configure_heater("k","H1",mode,**values);assert operations(t)==expected;assert t.calls[0][2]["parameters"]=={"block_name":"H1","value":mode}
def test_completion_semantics_fail_closed():
    for payload in ({"complete":True},{"input_complete":True},{"required_input_complete":True},{"input_state":"complete"}): assert is_explicitly_complete(payload)
    for payload in ({},{"success":True},{"complete":False},{"input_state":"unknown"},{"success":False,"complete":True}): assert not is_explicitly_complete(payload)
    t=Transport();t.queue=[{"input_complete":True},{"required_input_complete":True},{"run":"ok"}];assert AspenClient(transport=t).run("k")["run"]=="ok"

def test_execute_unwraps_canonical_envelope_only():
    t=Transport();t.queue=[{"status":"success","task_hash":"k","operation":"list_block_ports","result":{"success":True,"ports":{"F(IN)":[]}},"session_info":{"active":True}}]
    result=AspenClient(transport=t).execute("k","list_block_ports",block_name="M1")
    assert result=={"success":True,"ports":{"F(IN)":[]}}
    t.queue=[{"status":"started","task_hash":"k","result":{"should":"remain"}}]
    assert AspenClient(transport=t).start("k")["status"]=="started"

def test_methanol_sends_meoh_and_verifies_live_visible_id():
    t=Transport();t.queue=[
        {"status":"success","result":{"success":True,"components_added":[{"component_id":"MEOH","requested_component_id":"MEOH","cas":"67-56-1"}],"verification":{"success":True,"missing_component_ids":[]}}},
        {"status":"success","result":{"success":True,"rows":[{"component_id":"MEOH","cas":"67-56-1"}],"missing_requested_component_ids":[]}},
    ]
    result=AspenClient(transport=t).add_components("k",["METHANOL"])
    assert t.calls[0][2]["parameters"]["components"]==[{"component_id":"MEOH","cas":"67-56-1"}]
    assert t.calls[1][2]["parameters"]=={"component_ids":["MEOH"]}
    assert result["inspection"]["rows"][0]["component_id"]=="MEOH"

def test_component_verification_uses_returned_visible_id():
    t=Transport();t.queue=[
        {"result":{"success":True,"components_added":[{"component_id":"MEOH","requested_component_id":"METHANOL","cas":"67-56-1"}],"verification":{"success":True}}},
        {"result":{"success":True,"rows":[{"component_id":"MEOH"}],"missing_requested_component_ids":[]}},
    ]
    AspenClient(transport=t).add_components("k",["methanol"])
    assert t.calls[1][2]["parameters"]["component_ids"]==["MEOH"]

def test_block_methods_send_canonical_operation_names():
    t=Transport();client=AspenClient(transport=t)
    client.create_mixer_block("k","M1");client.create_heater_block("k","H1")
    assert operations(t)==["create_mixer","create_heater"]
    assert t.calls[0][2]=={"task_hash":"k","operation":"create_mixer","parameters":{"block_name":"M1"}}
    assert t.calls[1][2]=={"task_hash":"k","operation":"create_heater","parameters":{"block_name":"H1"}}

def test_next_status_sends_canonical_ui_operation():
    t=Transport();t.queue=[{"result":{"success":True,"required_input_complete":True}}]
    result=AspenClient(transport=t).next_status("k")
    assert result["required_input_complete"] is True
    assert t.calls[0][2]=={"task_hash":"k","operation":"ui_check_next_completion_status","parameters":{}}

def test_run_calls_canonical_next_gate_before_engine():
    t=Transport();t.queue=[{"result":{"input_complete":True}},{"result":{"required_input_complete":True}},{"result":{"run":"ok"}}]
    assert AspenClient(transport=t).run("k")["run"]=="ok"
    assert operations(t)==["check_flowsheet_completion","ui_check_next_completion_status","engine_run"]
    t=Transport();t.queue=[{"result":{"input_complete":True}},{"result":{"input_state":"unknown"}}]
    with pytest.raises(AspenError): AspenClient(transport=t).run("k")
    assert operations(t)==["check_flowsheet_completion","ui_check_next_completion_status"]

def test_material_stream_tp_exact_sequence_and_registry_ids():
    t=Transport();client=AspenClient(transport=t)
    result=client.configure_material_stream_tp("k","F1",temperature=300,temperature_unit="K",pressure=2,pressure_unit="bar",basis="MOLE-FLOW",component_flows={"water":1.5,"METHANOL":.5},flow_unit="kmol/hr")
    assert operations(t)==["set_mixed_spec_mixed","set_temp_mixed","set_pres_mixed","set_basis_mixed","set_flow_mixed","set_flow_mixed"]
    parameters=[call[2]["parameters"] for call in t.calls]
    assert parameters[0]=={"stream_name":"F1","value":"TP"}
    assert parameters[1]=={"stream_name":"F1","value":300,"unit":"K"}
    assert parameters[2]=={"stream_name":"F1","value":2,"unit":"bar"}
    assert parameters[3]=={"stream_name":"F1","value":"MOLE-FLOW"}
    assert parameters[4]=={"stream_name":"F1","component_name":"WATER","value":1.5,"unit":"kmol/hr"}
    assert parameters[5]=={"stream_name":"F1","component_name":"MEOH","value":.5,"unit":"kmol/hr"}
    assert result["component_ids"]==["WATER","MEOH"]

def test_material_stream_tp_checks_flows_and_basis():
    client=AspenClient(transport=Transport());common=dict(key="k",stream_name="F1",temperature=300,temperature_unit="K",pressure=1,pressure_unit="bar",flow_unit="kg/hr")
    with pytest.raises(ValueError): client.configure_material_stream_tp(**common,basis="MOLE-FRAC",component_flows={"water":1})
    with pytest.raises(ValueError): client.configure_material_stream_tp(**common,basis="MASS-FLOW",component_flows={"water":-1})
    with pytest.raises(ValueError): client.configure_material_stream_tp(**common,basis="MASS-FLOW",component_flows={"water":0})

def test_ui_next_uses_distinct_timeout_without_retry():
    t=Transport();t.queue=[{"result":{"required_input_complete":True}}];client=AspenClient(transport=t,timeout=10,ui_timeout=90);client.next_status("k")
    assert len(t.calls)==1
    assert t.timeouts==[90]

def test_next_gate_short_circuit_is_explicit_completion():
    payload={"success":True,"skipped":True,"guardrail_reason":"non_gui_short_circuit_engine_run_success","no_completion_issues":True,"diagnostic_kind":"required_input_complete","feedback_window_kind":"required_input_complete","engine_run":{"success":True},"message":"Required Input Complete"}
    assert is_explicitly_complete(payload)
    assert is_explicitly_complete({"success":True,"no_completion_issues":True,"diagnostic_kind":"required_input_complete"})
    assert not is_explicitly_complete({"success":True,"skipped":True})
    assert not is_explicitly_complete({"success":True,"no_completion_issues":True,"diagnostic_kind":"other"})
    assert not is_explicitly_complete({"success":False,"no_completion_issues":True,"diagnostic_kind":"required_input_complete"})

def test_run_reuses_next_gate_engine_short_circuit_without_duplicate():
    next_payload={"success":True,"skipped":True,"guardrail_reason":"non_gui_short_circuit_engine_run_success","no_completion_issues":True,"diagnostic_kind":"required_input_complete","feedback_window_kind":"required_input_complete","engine_run":{"success":True,"native_run_id":"run-1"}}
    t=Transport();t.queue=[{"result":{"input_complete":True}},{"result":next_payload}]
    result=AspenClient(transport=t).run("k")
    assert result=={"success":True,"native_run_id":"run-1","source":"next_gate_short_circuit"}
    assert operations(t)==["check_flowsheet_completion","ui_check_next_completion_status"]

def test_preflight_returns_both_payloads_once():
    t=Transport();t.queue=[{"result":{"input_complete":True}},{"result":{"required_input_complete":True}}]
    result=AspenClient(transport=t).preflight("k")
    assert result["completion"]["input_complete"] is True
    assert result["next_status"]["required_input_complete"] is True
    assert operations(t)==["check_flowsheet_completion","ui_check_next_completion_status"]

def test_canonical_evidence_export_sequence_and_parameters():
    t=Transport();client=AspenClient(transport=t);result=client.export_evidence("k","runs/case")
    assert operations(t)==["export_rep","export_apw"]
    assert t.calls[0][2]["parameters"]=={"export_format":2,"filename":"runs/case.rep"}
    assert t.calls[1][2]["parameters"]=={"filename":"runs/case.apw"}
    assert set(result)=={"rep","apw"}

def test_direct_canonical_exports_and_safe_names():
    t=Transport();client=AspenClient(transport=t);client.export_rep("k");client.export_apw("k")
    assert t.calls[0][2]["parameters"]=={"export_format":2}
    assert t.calls[1][2]["parameters"]=={}
    with pytest.raises(ValueError): client.export_evidence("k","../outside")
    with pytest.raises(ValueError): client.export_evidence("k","C:/outside")

def test_evidence_export_failure_is_not_hidden():
    class FailingTransport(Transport):
        def request(self,method,url,*,json=None,timeout=None):
            if json and json.get("operation")=="export_apw":
                response=Response({"detail":"apw failed"});response.status_code=500;return response
            return super().request(method,url,json=json,timeout=timeout)
    with pytest.raises(AspenError): AspenClient(transport=FailingTransport()).export_evidence("k","case")

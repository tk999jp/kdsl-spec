KDSL_RESULT:
SCHEMA:kdsl-r1c@0.1-draft
STATUS:partial
PHASE:VERIFY contradiction
S:same verification appears in pass and not_run
FILES:[]
WHY:verification classes must remain distinct
CMD:[]
VERIFY:{"pass":["target runtime"],"fail":[],"not_run":["target runtime"]}
RT:{"state":"p","basis":"target runtime未実行"}
RISK:["runtime_unverified"]
NEXT:{"proposal":"run target runtime","authority":"proposal_only"}
COMMIT:{"actual":null,"proposed":null,"permission_basis":"none"}

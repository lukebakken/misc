-module(test_badarg).

-export([run/0]).

run() ->
    Mod = 1234,
    Mod:is_empty(),
    halt().

%% reason: {badarg,
%%             [{erlang,apply,
%%                  [is_empty,[]],
%%                  [{error_info,#{module => erl_erts_errors}}]},
%%              {rabbit_mirror_queue_slave,process_instruction,2,
%%                  [{file,"rabbit_mirror_queue_slave.erl"},{line,992}]},
%%              {rabbit_mirror_queue_slave,handle_cast,2,
%%                  [{file,"rabbit_mirror_queue_slave.erl"},{line,359}]},
%%              {gen_server2,handle_msg,2,
%%                  [{file,"gen_server2.erl"},{line,1056}]},
%%              {proc_lib,wake_up,3,[{file,"proc_lib.erl"},{line,251}]}]}

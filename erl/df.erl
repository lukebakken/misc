-module(df).

-export([run/0]).

run() ->
    Exe = os:find_executable("df"),
    %% Args = ["/home"],
    %% Opts = [eof, exit_status, stream, stderr_to_stdout, {args, Args}],
    Opts = [eof, exit_status, stream, stderr_to_stdout],
    %% Opts = [eof, exit_status, {line, 1024}, stderr_to_stdout, {args, Args}],
    Port = erlang:open_port({spawn_executable, Exe}, Opts),
    Reply = get_reply(Port, []),
    io:format("Reply: ~tp~n", [Reply]),
    RV = catch erlang:port_close(Port),
    io:format("port_close RV: ~tp~n", [RV]).

get_reply(Port, Acc) ->
    receive
        {Port, {data, Data}} ->
            io:format("port data: ~tp~n", [Data]),
            get_reply(Port, Acc);
        {Port, {exit_status, Status}} ->
            io:format("port exited Status: ~tp~n", [Status]),
            Acc;
        {'EXIT', Port, Reason} ->
            exit({port_died, Reason});
        UnknownMsg ->
            io:format("port UnknownMsg: ~tp~n", [UnknownMsg])
    end.

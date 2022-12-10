-module(pwsh2).

-export([run/0]).

run() ->
    SystemRootDir = os:getenv("SystemRoot", "/"), 
    Pwsh = os:find_executable("pwsh.exe"), 
    
    Cmd = "Get-Process -Id " ++ os:getpid() ++ " | Select-Object -ExpandProperty HandleCount",
    A1 = ["-NoLogo",
          "-NonInteractive",
          "-NoProfile",
          "-InputFormat", "Text",
          "-OutputFormat", "Text",
          "-Command", Cmd],
    
    % Note: 'hide' must be used or this will not work!
    A0 = [binary, exit_status, stderr_to_stdout, in, hide,
          {cd, SystemRootDir}, {line, 512}, {arg0, Pwsh}, {args, A1}],

    Port = erlang:open_port({spawn_executable, Pwsh}, A0),
    MonRef = erlang:monitor(port, Port),
    case pwsh_receive(Port, MonRef, <<>>) of
        {ok, Data} ->
            io:format("Data: ~tp~n", [Data]);
        Error ->
            io:format("Error: ~tp~n", [Error])
    end,
    true = erlang:demonitor(MonRef, [flush]),
    ok.

pwsh_receive(Port, MonRef, Data0) ->
    receive
        {Port, {exit_status, 0}} ->
            catch erlang:port_close(Port),
            flush_until_down(Port, MonRef),
            {ok, Data0};
        {Port, {exit_status, Status}} ->
            catch erlang:port_close(Port),
            flush_until_down(Port, MonRef),
            {error, {exit_status, Status}};
        {Port, {data, {eol, Data1}}} ->
            pwsh_receive(Port, MonRef, Data1);
        {'DOWN', MonRef, _, _, _} ->
            flush_exit(Port),
            {error, nodata}
    after 5000 ->
        {error, timeout}
    end.

flush_until_down(Port, MonRef) ->
    receive
        {Port, {data, _Bytes}} ->
            flush_until_down(Port, MonRef);
        {'DOWN', MonRef, _, _, _} ->
            flush_exit(Port)
    after 500 ->
        flush_exit(Port)
    end.

flush_exit(Port) ->
    receive
        {'EXIT', Port, _} -> ok
    after 0 ->
        ok
    end.

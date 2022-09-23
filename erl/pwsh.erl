-module(pwsh).

-export([run/0]).

run() ->
    SystemRootDir = os:getenv("SystemRoot", "/"), 
    Pwsh = os:find_executable("powershell.exe"), 
    
    A1 = ["-NonInteractive", "-NoProfile", "-NoLogo", "-InputFormat", "Text", "-WindowStyle", "Hidden"],
    
    % Note: 'hide' must be used or this will not work!
    A0 = [use_stdio, stderr_to_stdout, {cd, SystemRootDir}, {line, 512}, hide, {args, A1}],

    P = erlang:open_port({spawn_executable, Pwsh}, A0),
    MonRef = erlang:monitor(port, P),

    Cmd = "(Get-PSDrive -Name C).Free",
    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(MonRef, P, Cmd),
    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(MonRef, P, Cmd),

    timer:sleep(2500), 

    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(MonRef, P, Cmd),
    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(MonRef, P, Cmd),

    ExitCmd = "exit 0",
    true = erlang:port_command(P, ExitCmd ++ "\n"),
    % sh_receive(MonRef, P, ExitCmd),

    true = erlang:demonitor(MonRef, [flush]),
    RV = catch erlang:port_close(P),
    io:format("port_close RV: ~p~n", [RV]).

% Data: "721756360704"
% Data0: "PS C:\\WINDOWS> (Get-PSDrive -Name C).Free"
% found cmd in output: "(Get-PSDrive -Name C).Free"
% Data: "721756217344"
sh_receive(MonRef, Port, Cmd) ->
    FoundCmd =  receive
                    {'DOWN', MonRef, port, Port, Info0} ->
                        io:format("Saw unexpected DOWN message! ~p~n", [Info0]);
                        % TODO: restart, re-try
                    {Port, {data, {eol, Data0}}} ->
                        io:format("Data0: ~p~n", [Data0]),
                        case string:find(Data0, Cmd, trailing) of
                            nomatch ->
                                {error, {unexpected, Data0}};
                            _ ->
                                io:format("found cmd in output: ~p~n", [Cmd]),
                                ok
                        end
                after 5000 ->
                          {error, timeout}
                end,
    case FoundCmd of
        ok ->
            receive
                {'DOWN', MonRef, port, Port, Info1} ->
                    io:format("Saw unexpected DOWN message! ~p~n", [Info1]);
                    % TODO: restart, re-try
                {Port, {data, {eol, Data1}}} ->
                    io:format("Data: ~p~n", [Data1])
            after 5000 ->
                      {error, timeout}
            end;
        Error ->
            io:format("Error: ~p~n", [Error]),
            Error
    end.

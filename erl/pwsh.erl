-module(pwsh).

-export([run/0]).

run() ->
    Pwsh = os:find_executable("pwsh.exe"), 
    
    A1 = ["-NonInteractive","-NoProfile","-NoLogo","-InputFormat","Text","-WindowStyle","Hidden"],
    
    A0 = [use_stdio,stderr_to_stdout,overlapped_io,{line,512},hide,{args, A1}],

    P = erlang:open_port({spawn_executable, Pwsh}, A0),

    Cmd = "(Get-PSDrive -Name C).Free",
    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(P, Cmd),
    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(P, Cmd),

    timer:sleep(2500), 

    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(P, Cmd),
    true = erlang:port_command(P, Cmd ++ "\n"),
    sh_receive(P, Cmd),

    ExitCmd = "exit 0",
    true = erlang:port_command(P, ExitCmd ++ "\n"),

    RV = erlang:port_close(P),
    io:format("port_close RV: ~p~n", [RV]).


sh_receive(Port, Cmd) ->
    FoundCmd =  receive
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
                {Port, {data, {eol, Data1}}} ->
                    io:format("Data: ~p~n", [Data1])
            after 5000 ->
                      {error, timeout}
            end;
        Error ->
            io:format("Error: ~p~n", [Error]),
            Error
    end.

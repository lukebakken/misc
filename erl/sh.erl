-module(sh).

-export([run/0]).

run() ->
    P = erlang:open_port({spawn_executable, "/bin/sh"}, [use_stdio,exit_status,stderr_to_stdout,{line,512},{args,["-s","-v"]}]),
    sh_receive(),
    true = erlang:port_command(P, "echo FOOFOO\n\n"),
    sh_receive(),
    true = erlang:port_command(P, "exit 0\n\n"),
    sh_receive(),
    RV = erlang:port_close(P),
    io:format("port_close RV: ~p~n", [RV]).


sh_receive() ->
    receive
        M -> io:format("M: ~p~n", [M]),
             sh_receive()
    after 500 ->
              io:format("receive timeout!~n"),
              ok
    end.

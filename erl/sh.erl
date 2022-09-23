-module(sh).

-export([run/0]).

run() ->
    Args = ["-s", "rabbit_disk_monitor"],
    Opts = [stream, stderr_to_stdout, {args, Args}],
    Port = erlang:open_port({spawn_executable, "/bin/sh"}, Opts),

    CmdUtf8 = <<"/usr/bin/df -kP '/home/lbakken/development/lukebakken/rabbitmq/server/5551/RabbitMQ Sérvér - Евгений/db/rabbit@shostakovich'"/utf8>>,
    % CmdUtf8 = <<"/usr/bin/df -kP '/home/lbakken/development/lukebakken/rabbitmq'"/utf8>>,

    ok = file:write_file("/tmp/cmd.sh", CmdUtf8),

    Cmd = unicode:characters_to_binary(io_lib:format("(~ts~n) < /dev/null; echo  \"\^M\"~n", [CmdUtf8])),
    % Cmd = io_lib:format("(~ts~n) < /dev/null > /tmp/df.txt; echo  \"\^M\"~n", [CmdUtf8]),
    % Cmd = ". /tmp/cmd.sh < /dev/null > /tmp/df.txt; echo  \"\^M\"\n",

    Port ! {self(), {command, [Cmd, 10]}}, % The 10 at the end is a newline
    Reply = get_reply(Port, []),
    io:format("Reply: ~tp~n", [Reply]),

    % {ok, Df} = file:read_file("/tmp/df.txt"),
    % io:format("df.txt: ~tp~n", [Df]),

    RV = erlang:port_close(Port),
    io:format("port_close RV: ~tp~n", [RV]).

get_reply(Port, O) ->
    receive
        {Port, {data, N}} ->
            case newline(N, O) of
                {ok, Str} ->
                    Str;
                {more, Acc} ->
                    get_reply(Port, Acc)
            end;
        {'EXIT', Port, Reason} ->
            exit({port_died, Reason})
    end.

% Character 13 is ^M or carriage return
newline([13|_], B) ->
    {ok, lists:reverse(B)};
newline([H|T], B) ->
    newline(T, [H|B]);
newline([], B) ->
    {more, B}.

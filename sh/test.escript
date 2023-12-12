#!/usr/bin/env escript
%% -*- erlang -*-
%%! -noinput -sname test_escript -mnesia debug verbose
main(Args) ->
    try
        io:format("Args ~tp~n", [Args]),
        timer:sleep(30000)
    catch
        _:_ ->
            usage()
    end.

usage() ->
    io:format("usage: test input0 input1\n"),
    halt(1).

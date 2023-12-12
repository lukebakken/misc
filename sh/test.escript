#!/usr/bin/env escript
%% -*- erlang -*-
%%! -noinput -sname test_escript -mnesia debug verbose
main(Args) ->
    try
        io:format("Args ~tp~n", [Args])
    catch
        _:_ ->
            usage()
    end;
main(_) ->
    usage().

usage() ->
    io:format("usage: test input0 input1\n"),
    halt(1).

-module(test_badarg).

-export([run/0]).

run() ->
    State = [],
    Mod = mod_one,
    Mod:is_empty(State),
    init:stop().

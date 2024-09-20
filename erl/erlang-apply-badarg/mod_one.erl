-module(mod_one).

-export([is_empty/1]).

-record(vqstate, {foo = 0 :: integer()}).

is_empty(#vqstate{foo = FooVal}) ->
    FooVal =:= 0;
is_empty(Arg) when is_list(Arg) ->
    0 == Arg.

defmodule Testex do
  @moduledoc """
  Documentation for `Testex`.
  """

  @doc """
  Hello world.

  ## Examples

      iex> Testex.hello()
      :world

  """
  def hello do
    :world
  end

  def main(args)
  do
    IO.puts("@@@@@@@@ args: #{args}")
    Process.sleep(10000)
  end
end

defmodule Day1 do
  def fuel(x) do
    max(div(x, 3) - 2, 0)
  end

  def fuel_rec(x, acc) do
    case fuel(x) do
      0 -> acc
      f -> fuel_rec(f, acc+f)  
    end
  end
end

modules = File.read!("data.txt")
  |> String.split
  |> Enum.map(&String.to_integer/1)


IO.puts Day1.fuel_rec(14, 0)
IO.puts "part 1: #{Enum.map(modules, fn x -> Day1.fuel(x) end) |> Enum.sum}"
IO.puts "part 2: #{Enum.map(modules, fn x -> Day1.fuel_rec(x, 0) end) |> Enum.sum}"
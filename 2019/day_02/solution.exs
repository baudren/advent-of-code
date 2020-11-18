program_orig = File.read!("data.txt") |> String.trim() |> String.split(",") |> Enum.map(&String.to_integer/1)

program_orig = List.replace_at(List.replace_at(program_orig, 1, 12), 2, 2)

defmodule Day2 do
  def run_sequence(program, index \\ 0) do
    opcode = Enum.at(program, index)
    case opcode do
      99 -> Enum.at(program, 0)
      1 -> run_sequence(
        List.replace_at(program, Enum.at(program, index+3), Enum.at(program, Enum.at(program, index+1)) + Enum.at(program, Enum.at(program, index+2))),
        index+4
      )
      2 -> run_sequence(
        List.replace_at(program, Enum.at(program, index+3), Enum.at(program, Enum.at(program, index+1)) * Enum.at(program, Enum.at(program, index+2))),
        index+4
      )
    end
  end

  def search_output(program, output) do
    try do
      for i <- 0..99 do
        for j <- 0..99 do
          if run_sequence(List.replace_at(List.replace_at(program, 1, i), 2, j)) == output do
            throw([i, j])
          else
            [i, j]
          end
        end
      end
    catch
      [noun, verb] -> IO.puts 100*noun+verb
    end
  end
end

IO.inspect Day2.run_sequence(program_orig)
IO.inspect Day2.search_output(program_orig, 19690720)

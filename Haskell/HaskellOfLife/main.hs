

main :: IO ()
main = do
    let width = 5
    let height = 5

    putStrLn $ "World dimensions: " ++ (show width) ++ " x " ++ (show height)

    let world = [".####", "#.###", "##.##", "###.#", "####."]

    putStrLn $ head world

    
    putStrLn "END!"


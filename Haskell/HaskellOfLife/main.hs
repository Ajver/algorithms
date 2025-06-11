
showWorld :: [String] -> IO ()
showWorld [] = putStrLn ""
showWorld [a] = putStrLn a
showWorld (w:rest) = do 
    putStrLn w  
    showWorld rest


main :: IO ()
main = do
    let width = 5
    let height = 5

    putStrLn $ "World dimensions: " ++ (show width) ++ " x " ++ (show height)

    let world = [".####", "#.###", "##.##", "###.#", "####."]

    showWorld world
    
    putStrLn "END!"


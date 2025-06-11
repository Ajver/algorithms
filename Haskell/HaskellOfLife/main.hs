

main :: IO ()
main = do
    putStrLn "Set World width: "
    input <- getLine
    let width = read input :: Int

    putStrLn "Set World height: "
    input <- getLine
    let height = read input :: Int

    putStrLn $ "World dimensions: " ++ (show width) ++ " x " ++ (show height)

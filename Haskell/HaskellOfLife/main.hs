
showWorld :: [String] -> IO ()
showWorld [] = putStrLn ""
showWorld [a] = putStrLn a
showWorld (w:rest) = do 
    putStrLn w  
    showWorld rest


countIfAlive :: Char -> Int
countIfAlive '#' = 1
countIfAlive _ = 0

countInRow :: String -> String -> Int
countInRow [] right = (countIfAlive $ head right)
countInRow left [] = (countIfAlive $ last left)
countInRow left right = (countIfAlive $ last left) + (countIfAlive $ head right)

countWholeRow :: String -> [Int]
countWholeRow row = [(countInRow (take (x-1) row) (drop x row)) | x <- [1..5]]

countNeighbours :: [String] -> [[Int]]
countNeighbours world =
    [(countWholeRow r) | r <- world]

    
   
    

main :: IO ()
main = do
    let width = 5
    let height = 5

    putStrLn $ "World dimensions: " ++ (show width) ++ " x " ++ (show height)

    let world = [".####", "#.###", "##.##", "###.#", "####."]

    showWorld world
    let foo = countNeighbours world
    putStrLn $ show foo
    putStrLn "END!"


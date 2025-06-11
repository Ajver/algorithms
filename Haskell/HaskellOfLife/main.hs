
getElement :: (Ord a) => [a] -> Int -> a
getElement elements idx = head (drop (idx-1) elements)

showWorld :: [String] -> IO ()
showWorld [] = putStrLn ""
showWorld [a] = putStrLn a
showWorld (w:rest) = do 
    putStrLn w  
    showWorld rest

add2Lists :: [Int] -> [Int] -> [Int]
add2Lists ta tb = [(fst x + snd x) | x <- (zip ta tb)] 

add3Lists :: [Int] -> [Int] -> [Int] -> [Int]
add3Lists a b c = add2Lists a $ add2Lists b c

countIfAlive :: Char -> Int
countIfAlive '#' = 1
countIfAlive _ = 0

countInRow :: String -> String -> Int
countInRow [] right = (countIfAlive $ head right)
countInRow left [] = (countIfAlive $ last left)
countInRow left right = (countIfAlive $ last left) + (countIfAlive $ head right)

countWholeRow :: String -> [Int]
countWholeRow [] = [0, 0, 0, 0, 0]
countWholeRow row = [(countInRow (take (x-1) row) (drop x row)) | x <- [1..5]]

countWholeRowIncludingThemself :: String -> [Int]
countWholeRowIncludingThemself [] = [0, 0, 0, 0, 0]
countWholeRowIncludingThemself row = [(countInRow (take (x-1) row) (drop x row)) + (countIfAlive (getElement row x)) | x <- [1..5]]

countNeighbours :: [String] -> [[Int]]
countNeighbours world = 
    let first = add2Lists (countWholeRow $ getElement world 1) (countWholeRowIncludingThemself $ getElement world 2)
        middle = [add3Lists (countWholeRowIncludingThemself $ getElement world (idx-1)) (countWholeRow $ getElement world idx) (countWholeRowIncludingThemself $ getElement world (idx+1)) | idx <- [2..4]]
        last = add2Lists (countWholeRowIncludingThemself $ getElement world 4) (countWholeRow $ getElement world 5)
    in [first] ++ middle ++ [last]


main :: IO ()
main = do
    let width = 5
    let height = 5

    putStrLn $ "World dimensions: " ++ (show width) ++ " x " ++ (show height)

    let world = ["#####", "#.###", "##.##", "###.#", "#####"]

    showWorld world
    let foo = countNeighbours world
    putStrLn $ show foo
    putStrLn "END!"


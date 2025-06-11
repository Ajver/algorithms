-- helper func 
getElement :: (Ord a) => [a] -> Int -> a
getElement elements idx = head (drop (idx-1) elements)

add2Lists :: [Int] -> [Int] -> [Int]
add2Lists ta tb = [(fst x + snd x) | x <- (zip ta tb)] 

add3Lists :: [Int] -> [Int] -> [Int] -> [Int]
add3Lists a b c = add2Lists a $ add2Lists b c

-- world func
showWorld :: [String] -> IO ()
showWorld [] = putStrLn ""
showWorld [a] = putStrLn a
showWorld (w:rest) = do 
    putStrLn w  
    showWorld rest

-- TODO: implement getting world


-- mechanics of the game
countIfAlive :: Char -> Int
countIfAlive state = if state == '#' then 1 else 0

countNeighbourForCellInOneRow :: String -> Int -> Int
countNeighbourForCellInOneRow row 1 = (countIfAlive $ getElement row 2)
countNeighbourForCellInOneRow row 5 = (countIfAlive $ getElement row 4)
countNeighbourForCellInOneRow row idx = (countIfAlive $ getElement row (idx - 1)) + (countIfAlive $ getElement row (idx + 1))

countNeigboursInRow :: String -> [Int]
countNeigboursInRow row = [countNeighbourForCellInOneRow row x | x <- [1 .. 5]]

countNeighboursInRowIncludingThemselves :: String -> [Int]
countNeighboursInRowIncludingThemselves row = [countNeighbourForCellInOneRow row x + (countIfAlive (getElement row x)) | x <- [1..5]]

countRowAndSurrounding :: [String] -> Int -> [Int]
countRowAndSurrounding world 0 = add2Lists (countNeigboursInRow $ getElement world 1) (countNeighboursInRowIncludingThemselves $ getElement world 2)
countRowAndSurrounding world 5 = add2Lists (countNeighboursInRowIncludingThemselves $ getElement world 4) (countNeigboursInRow $ getElement world 5)
countRowAndSurrounding world rowIdx = add3Lists (countNeighboursInRowIncludingThemselves $ getElement world (rowIdx-1)) (countNeigboursInRow $ getElement world rowIdx) (countNeighboursInRowIncludingThemselves $ getElement world (rowIdx+1))

countNeighbours :: [String] -> [[Int]]
countNeighbours world = [countRowAndSurrounding world idx | idx <- [1..5]]

al :: Char -> Int -> Char
al state count
    | state == '#' && (count < 2) = '.'
    | state == '#' && (count > 3) = '.'
    | state == '.' && (count == 3) = '#'
    | otherwise = state

applyLogic :: (Char, Int) -> Char
applyLogic tuple = al (fst tuple) (snd tuple)

applyLogicForRow :: String -> [Int] -> String
applyLogicForRow r c = map (applyLogic) (zip r c)

performeEvolutionStep :: [String] -> [String]
performeEvolutionStep world =
    let count = countNeighbours world
    in logic world count

live_Cycyle :: [String] -> Int -> IO ()
live_Cycyle _ 0 = putStrLn "END!"
live_Cycyle world n = do
    let newWorld = performeEvolutionStep world

    showWorld world
    putStrLn ""
    live_Cycyle newWorld (n-1)

    


logic :: [String] -> [[Int]] -> [String]
logic world counts = [applyLogicForRow (getElement world idx) (getElement counts idx) | idx <- [1..5]]

main :: IO ()
main = do
    let width = 5
    let height = 5
    let epoch = 10
    putStrLn $ "World dimensions: " ++ (show width) ++ " x " ++ (show height)

    let world = [".....", ".....", ".###.", ".....", "....."]

    
    live_Cycyle world epoch

    


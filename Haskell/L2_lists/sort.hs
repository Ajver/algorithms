listMin :: [Int] -> Int
listMin [x]      = x
listMin (x:xs)   = min x (listMin xs)


listMax :: [Int] -> Int
listMax [x] = x
listMax (x:xs) = max x (listMax xs)


filterGreaterThan :: Int -> [Int] -> [Int]
filterGreaterThan a nums = [x | x <- nums, x > a]

listToStr :: [Int] -> String
listToStr [] = ""
listToStr [x] = show x
listToStr (x:xs) = (show x) ++ " " ++ (listToStr xs)

doubleElements :: [Int] -> [Int]
doubleElements [] = []
doubleElements (x:xs) = [x, x] ++ (doubleElements xs)


-- scal dwie (posortowane) listy
merge :: Ord a => [a] -> [a] -> [a]
merge xs [] = xs
merge [] ys = ys
merge (x:xs) (y:ys)
  | x <= y = x : merge xs (y:ys)
  | otherwise = y : merge (x:xs) ys

halve :: [a] -> ([a],[a])
halve xs = (take half xs, drop half xs)
    where half = length xs `div` 2


-- sortowanie przez scalanie
mergeSort :: [Int] -> [Int]
mergeSort [] = []
mergeSort [x] = [x]
mergeSort xs = merge (mergeSort (fst halves)) (mergeSort (snd halves))
    where halves = halve xs
  
  


main :: IO ()
main = do
    input <- getLine
    let nums = map read (words input) :: [Int]
    putStrLn $ (show $ listMin nums) ++ " " ++ (show $ listMax nums)
    putStrLn $ listToStr $ filterGreaterThan 10 nums
    putStrLn $ listToStr $ doubleElements nums
    putStrLn $ listToStr $ mergeSort nums
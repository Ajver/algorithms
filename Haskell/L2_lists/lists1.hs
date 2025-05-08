
listToStr :: [Int] -> String
listToStr [] = ""
listToStr [x] = show x
listToStr (x:xs) = (show x) ++ " " ++ (listToStr xs)


floatListToStr :: [Float] -> String
floatListToStr [] = ""
floatListToStr [x] = show x
floatListToStr (x:xs) = (show x) ++ " " ++ (floatListToStr xs)


reverseList [] = []
reverseList (x:xs) = reverseList xs ++ [x]

toChar :: Int -> Char
toChar = toEnum


-- Funkcja main
main :: IO ()
main = do
    input <- getLine
    let n = read input :: Int
    putStrLn $ listToStr [n..(n+20)]
    putStrLn $ listToStr (reverseList ([(n+2)..(n+15)]))
    let nFloat = fromIntegral n :: Float
    putStrLn $ floatListToStr [(fromIntegral n :: Float) + (i * 0.125) | i <- [0..(16 * 8)]]
    putStrLn $ show $ [toChar (97 + i) | i <- [0..25], i `mod` 2 == 0]
    

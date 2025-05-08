isLeapYear :: Int -> Bool
isLeapYear year = ((year `mod` 4 == 0) && (year `mod` 100 /= 0)) || (year `mod` 400 == 0)


smallestPrimeFactor :: Int -> Int
smallestPrimeFactor n = pf 2 n

pf :: Int -> Int -> Int
pf a n
 | n `mod` a == 0 = a
 | otherwise = pf (a + 1) n


-- Funkcja main
main :: IO ()
main = do
    input <- getLine
    let year = read input :: Int
    if isLeapYear year
       then putStrLn "TAK"
       else putStrLn "NIE"
    putStrLn $ show $ smallestPrimeFactor year
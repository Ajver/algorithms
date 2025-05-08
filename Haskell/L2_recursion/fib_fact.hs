fib :: Int -> Integer
fib 0 = 0
fib 1 = 1
fib n = fib (n - 1) + fib (n - 2)


fact :: Int -> Integer
fact n
  | n == 0 = 1
  | otherwise = (toInteger n) * fact (n - 1)


main :: IO ()
main = do
    line <- getLine
    let n = read line :: Int
    putStrLn $ show $ fact n
    putStrLn $ show $ fib n

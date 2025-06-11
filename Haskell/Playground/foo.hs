
pole :: Int -> Int -> Int
pole a h = (a * h) `div` 2

poleF :: Float -> Float -> Float
poleF a h = (a * h) / 2

dzieler :: Int -> Int -> Int
dzieler a 0 = -1
dzieler a b = a `div` b

dzielerG :: Int -> Int -> Int
dzielerG a b
  | b == 0 = -1
  | otherwise = a `div` b
  
znak :: Int -> String
znak a
  | a < 0 = "ujemna"
  | a > 0 = "dodatnia"
  | otherwise = "zero"

sprawdz_parzystosc :: Int -> String
sprawdz_parzystosc a 
  | a `mod` 2 == 0 = "parzysta"
  | otherwise = "nieparzysta"

czy0_10_lub_15plus :: Int -> Bool
czy0_10_lub_15plus a = (a >= 0 && a <= 10) || (a > 15)


twoj_stary :: Int -> Int -> Int
twoj_stary a b = twoja_stara a b 0

twoja_stara :: Int -> Int -> Int -> Int
twoja_stara a b c
    | a < b = c
    | otherwise = twoja_stara (a-b) b (c+1)


quick_sort :: (Ord a) => [a] -> [a]
quick_sort [] = []
quick_sort [a] = [a]
quick_sort (x:xs) =
    let left = [a | a <- xs, a <= x]
        right = [a | a <- xs, a > x]
    in (quick_sort left) ++ [x] ++ (quick_sort right)

check_sorted :: (Ord a) => [a] -> Bool
check_sorted [] = True
check_sorted [a] = True
check_sorted (x:xs) = (x <= head xs) && (check_sorted xs)

main :: IO ()
main = do
    putStrLn $ show $ pole 3 4
    putStrLn $ show $ poleF 3 4
    putStrLn $ show $ dzieler 10 0
    putStrLn $ show $ dzieler 10 4
    putStrLn $ show $ dzielerG 10 4
    putStrLn $ show $ znak 4
    putStrLn $ show $ znak (-4)
    putStrLn $ show $ znak (-0)
    putStrLn $ show $ sprawdz_parzystosc 4
    putStrLn $ show $ sprawdz_parzystosc 5
    
    -- if sprawdz_parzystosc 5 == "parzysta"
    -- then putStrLn "podzielna przez 2!"
    -- else putStrLn "jednak nie :c"
    
    
    -- map putStrLn $ map czy0_10_lub_15plus [-3..17]
    
    
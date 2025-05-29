-- Definicja typu binarnego drzewa przeszukiwań
data BST a = Empty
           | Node a (BST a) (BST a)
           deriving (Show, Eq)

-- Dodanie nowego elementu do drzewa
insert :: (Ord a) => a -> BST a -> BST a
insert x Empty = Node x Empty Empty
insert x (Node y left right)
    | x < y     = Node y (insert x left) right
    | x > y     = Node y left (insert x right)
    | otherwise = Node y left right -- Nie umieszczamy w drzewie duplikatów

-- Wyszukanie elementu w drzewie
search :: (Ord a) => a -> BST a -> Bool
search _ Empty = False
search x (Node y left right)
    | x == y    = True
    | x < y     = search x left
    | otherwise = search x right

-- Przeglądanie drzewa w porządku
inOrder :: BST a -> [a]
inOrder Empty = []
inOrder (Node y left right) = inOrder left ++ [y] ++ inOrder right


-- Znajdź minimum w niepustym drzewie BST
findMin :: BST a -> a
findMin (Node x Empty _) = x
findMin (Node x left _) = findMin left

joinBST :: (Ord a) => BST a -> BST a -> BST a -- połącz dwa drzewa (gdy wszystkie elementy z pierwszego są mniejsze od elementów z drugiego)
joinBST Empty Empty = Empty -- Brak dzieci: puste drzewo
joinBST Empty right = right -- Tylko prawe dziecko
joinBST left Empty = left -- Tylko lewe dziecko
joinBST left right =  -- Dwoje dzieci: najmniejszy element w prawym poddrzewie jest przenoszony do korzenia
    let minRight = findMin right
    in Node minRight left (delete minRight right)  -- TODO: Na pewno delete right???

-- Usuń element z BST
delete :: (Ord a) => a -> BST a -> BST a
delete _ Empty = Empty
delete x (Node y left right)
    | x < y  = Node y (delete x left) right    -- x jest w lewym poddrzewie
    | x > y  = Node y left (delete x right)    -- x jest w prawym poddrzewie
    | otherwise = joinBST left right -- x jest w korzeniu



-- Funkcja main
main :: IO ()
main = do
    input <- getLine
    let values1 = map read (words input) :: [Int]
    input <- getLine
    let values2 = map read (words input) :: [Int]
    let bst = foldr insert Empty values1
    print $ inOrder bst
    print $ [v | v <- values2, search v bst]
    let bst2 = foldr delete bst values2
    print $ inOrder bst2
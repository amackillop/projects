import scala.annotation.tailrec


object Main extends App {
  val result = Problems.penultimate(List(1))
  println(result)
}

object Problems {
  // P01
  def getLast[A](list: List[A]): Option[A] = list match {
    case x :: Nil => Some(x)
    case _ :: xs => getLast(xs)
    case _ => None
  }

  //P02
  def penultimate[A](list: List[A]): Option[A] = list match {
    case a :: b :: Nil => Some(a)
    case _ :: tail => penultimate(tail)
    case _ => None
  }

  //P03
  def nth[A](n: Int, list: List[A]): Option[A] = (n, list) match {
    case (0, x :: _) => Some(x)
    case (n, _ :: xs) => nth(n - 1, xs)
    case (_, Nil) => None
  }

  //P04
  def length[A](list: List[A]): Int = {
    (0 /: list) { (len, _) => len + 1 }
  }

  //P05
  def reverse[A](list: List[A]): List[A] = {
    (List[A]() /: list) { (xs, x) => x +: xs }
  }

  //P06
  def isPalindrome[A](list: List[A]): Boolean = {
    reverse(list) == list
  }

  //P07
  def flatten(list: List[Any]): List[Any] = list flatMap {
    case l: List[Any] => flatten(l)
    case e: Any => List(e)
  }

  //P08
  def compress[A](list: List[A]): List[A] = (list.init :\ List(list.last)) {
    (x, xs) => if (x != xs.head) x +: xs else xs
  }

  def compress2[A](list: List[A]): List[A] = {
    val (group, rest) = list span (_ == list.head)
    rest match {
      case Nil => List(group.head)
      case _ => group.head +: compress2(rest)
    }
  }

  //P09
  def pack[A](list: List[A]): List[List[A]] = (list.init :\ List(List(list.last))) {
    (x, xs) => if (x == xs.head.head) (x +: xs.head) +: xs.tail else List(x) +: xs
  }

  def pack2[A](list: List[A]): List[List[A]] = {
    val (group, rest) = list span (_ == list.head)
    rest match {
      case Nil => List(group)
      case _ => group +: pack2(rest)
    }
  }

  def pack3[A](list: List[A]): List[List[A]] = list match {
    case x :: xs => {
      val (group, rest) = list.tail span (_ == list.head)
      (list.head +: group) +: pack3(rest)
    }
    case Nil => Nil
  }

  //P10
  def encode[A](list: List[A]): List[(Int, A)] = {
    pack(list) map { (xs) => (xs.length, xs.head) }
  }

  //P11
  def encodeModified[A](list: List[A]): List[Any] = pack(list) map {
    (xs) => if (xs.length == 1) xs.head else (xs.length, xs.head)
  }

  //P12
  def decode[A](list: List[(Int, A)]): List[A] = {
    list flatMap { e => List.fill(e._1)(e._2) }
  }

  //P13
  def encodeDirect[A](list: List[A]): List[(Int, A)] = {
    val (pack, rest) = list span (_ == list.head)
    (pack.length, pack.head) +: encodeDirect(rest)
  }

  //P14
  def duplicate[A](list: List[A]): List[A] = {
    list flatMap { (x) => List(x, x) }
  }

  //P15
  def duplicateN[A](n: Int)(list: List[A]): List[A] = {
    list flatMap { (x) => List.fill(n)(x) }
  }

  //P16
  def dropEveryNth[A](n: Int)(list: List[A]): List[A] = for {
    (x, i) <- list.zipWithIndex if (i + 1) % n != 0
  } yield x

  //P17
  def split[A](n: Int)(list: List[A]): (List[A], List[A]) = {
    (list take n, list drop n)
  }

  def splitRecursive[A](n: Int)(list: List[A]): (List[A], List[A]) = {
    @tailrec
    def splitR(n: Int, left: List[A], right: List[A]): (List[A], List[A]) = (n, right) match {
      case (_, Nil) => (left.reverse, Nil)
      case (0, _) => (left.reverse, right)
      case (n, _) => splitR(n - 1, right.head :: left, right.tail)
    }

    splitR(n, Nil, list)
  }

  //P18
  def slice[A](start: Int, stop: Int, list: List[A]): List[A] = {
    (list drop start) take (stop - (start max 0))
  }

  //P19
  def rotate[A](n: Int)(list: List[A]): List[A] = {
    if (n >= 0) {
      val (left, right) = list.splitAt(n)
      right ::: left
    } else {
      val (left, right) = list.splitAt(list.length + n)
      right ::: left
    }
  }

  //P20
  def removeAt[A](n: Int)(list: List[A]): (List[A], Option[A]) = list.splitAt(n) match {
    case (_, Nil) => (list, None)
    case (Nil, right) => (right.tail, Some(right.head))
    case (left, right) => (left ::: right.tail, Some(right.head))
  }

  //P21
  def insertAt[A](n: Int)(elem: A, list: List[A]): List[A] = list.splitAt(n) match {
    case (left, right) => left ::: (elem :: right)
  }

  //P22
  def range(start: Int, stop: Int): List[Int] = {
    @tailrec def rng(stop: Int, list: List[Int]): List[Int] = {
      if (stop < start) list else rng(stop - 1, stop :: list)
    }

    rng(stop, Nil)
  }

  //P23
  def randInt(below: Int) = {
    scala.util.Random.nextInt(below)
  }

  // With resampling
  def randSelect[A](n: Int)(xs: List[A]): List[A] = {
    val limit = xs.length

    @tailrec
    def pickRand(n: Int, xs: List[A], picks: List[A]): List[A] = {
      n match {
        case 0 => picks
        case n => {
          val pick = xs(randInt(limit))
          pickRand(n - 1, xs, pick :: picks)
        }
      }
    }

    pickRand(n, xs, Nil)
  }

  // Without resampling
  def chooseN[A](n: Int)(xs: List[A]): List[A] = {
    @tailrec
    def pickRand[A](n: Int, xs: List[A], picks: List[A]): List[A] = {
      (n, xs) match {
        case (0, _)   => picks
        case (_, Nil) => picks
        case (n, xs)  => {
          val (rest, pick) = removeAt(randInt(xs.length))(xs)
          pickRand(n - 1, rest, pick.get :: picks)
        }
      }
    }

    pickRand(n, xs, Nil)
  }

  //P24
  def lotto(choose: Int, from1to: Int): List[Int] = {
    chooseN(choose)(range(1, from1to))
  }

  //P25
  def randomPermute[A](xs: List[A]): List[A] = {
    chooseN(xs.length)(xs)
  }

  //TODO: Implement a more efficient solution for P25

  //P26
//  def combinations[A](xs: List[A], chooseN: Int): List[List[A]] = (xs, chooseN) match {
//    case (_, 0)  => List(Nil)
//    case (xs, 1) => xs.map(List(_))
//    case _ => List(Nil)
//  }

  def flatMapSublists[A,B](ls: List[A])(f: (List[A]) => List[B]): List[B] = {
    @tailrec
    def loop(ls: List[A], f: List[A] => List[B], accum: List[B]): List[B] =
      ls match {
        case Nil => accum
        case sublist@(_ :: tail) => loop(tail, f, accum ::: f(sublist))
      }

    loop(ls, f, Nil)
  }

  def combinations[A](n: Int, ls: List[A]): List[List[A]] =
    if (n == 0) List(Nil)
    else flatMapSublists(ls) { sl =>
      combinations(n - 1, sl.tail) map {sl.head :: _}
    }

}


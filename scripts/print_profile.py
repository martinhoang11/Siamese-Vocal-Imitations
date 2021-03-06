import sys

import pstats


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    col = sys.argv[2] if len(sys.argv) > 2 else 'cumulative'
    p = pstats.Stats('profile.pstat')
    p.sort_stats(col).print_stats(n)


if __name__ == '__main__':
    main()

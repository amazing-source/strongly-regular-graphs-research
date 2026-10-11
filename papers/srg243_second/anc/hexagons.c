/* Count induced 6-cycles (hexagons) of a graph given as an edge list on n <= 256 vertices.
   Each cycle is counted once: v0 = smallest vertex, orientation fixed by v1 < v5.
   Usage: ./hexagons FILE.edges N K   (prints the count and Reimbayev's lower bound nk(k-2)(2k^2-21k+53)/12). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef struct { uint64_t w[4]; } bs;
static bs N[256]; static int nb[256][256], deg[256];
static int has(const bs *b, int i) { return (b->w[i >> 6] >> (i & 63)) & 1; }
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); int n = atoi(argv[2]); long long k = atoll(argv[3]); int a, b;
    while (fscanf(f, "%d %d", &a, &b) == 2) {
        N[a].w[b >> 6] |= 1ULL << (b & 63); N[b].w[a >> 6] |= 1ULL << (a & 63);
        nb[a][deg[a]++] = b; nb[b][deg[b]++] = a;
    }
    long long H = 0;
    for (int v0 = 0; v0 < n; v0++)
      for (int i1 = 0; i1 < deg[v0]; i1++) { int v1 = nb[v0][i1]; if (v1 < v0) continue;
        for (int i2 = 0; i2 < deg[v1]; i2++) { int v2 = nb[v1][i2]; if (v2 < v0 || v2 == v0 || has(&N[v0], v2)) continue;
          for (int i3 = 0; i3 < deg[v2]; i3++) { int v3 = nb[v2][i3];
            if (v3 < v0 || v3 == v1 || has(&N[v0], v3) || has(&N[v1], v3)) continue;
            for (int i4 = 0; i4 < deg[v3]; i4++) { int v4 = nb[v3][i4];
              if (v4 < v0 || v4 == v2 || has(&N[v0], v4) || has(&N[v1], v4) || has(&N[v2], v4)) continue;
              for (int i5 = 0; i5 < deg[v4]; i5++) { int v5 = nb[v4][i5];
                if (v5 <= v1 || v5 == v3 || !has(&N[v0], v5) || has(&N[v1], v5) || has(&N[v2], v5) || has(&N[v3], v5)) continue;
                H++; } } } } }
    long long bound = n * k * (k - 2) * (2 * k * k - 21 * k + 53) / 12;
    printf("%s: induced hexagons H = %lld, Reimbayev bound = %lld, H - bound = %lld\n", argv[1], H, bound, H - bound);
    return 0;
}

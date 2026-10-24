/* These are data structure maintenance routines with no original
 * content. They were written by command of the author while he
 * was ill in bed. */

/* Commit.c -- the shared commit-path helper (proposed name; the
 * author may rename it). One template, with a direction flag:
 * mark one way, unmark the other. Mark.c and Unmark.c are thin
 * wrappers over it. It lives as its own .c file, compiled and
 * linked normally -- no .c file is ever included.
 *
 * Settled shape: start S, count L, end E = S + L - 1; first and
 * last row by division by 32, first and last plane by division by
 * 1024. First edge row and last edge row take one masked word op
 * each (OR to mark, AND with the complement to unmark) plus a
 * partial counter add or subtract. Middle rows go by a single
 * memset over the range (0xFF / 0x00), their counters assigned
 * 32 / 0; middle planes assigned 1024 / 0. Edge planes move by
 * arithmetic: edge partials plus 32 per middle row inside the
 * plane. Check-then-set guards every flip: edge words on their
 * bits, middle ranges on their counters. Any check that fails
 * returns FAIL_OVERLAY and flips nothing.
 *
 * Implementation pending the author's word: blackboard Q4 (the
 * single-row collapse) and confirmation of the detailed design. */

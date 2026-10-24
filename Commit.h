/* These are data structure maintenance routines with no original
 * content. They were written by command of the author while he
 * was ill in bed. */

/* Commit.h -- declaration of the shared commit-path helper.
 * The helper lives in Commit.c, compiled and linked normally;
 * Mark.c and Unmark.c call it through this header. Never
 * #include a .c file. */

#ifndef ISCANDAR_COMMIT_H
#define ISCANDAR_COMMIT_H

#include <stdint.h>

/* Direction flag for commit_sectors: one template, two
 * directions. The helper name is proposed; the author may
 * rename it. */
#define COMMIT_UNMARK 0
#define COMMIT_MARK 1

int32_t commit_sectors(uint32_t *sectors, uint32_t *count_rows,
                       uint32_t *count_planes, uint32_t start,
                       uint32_t count, int direction);

#endif /* ISCANDAR_COMMIT_H */

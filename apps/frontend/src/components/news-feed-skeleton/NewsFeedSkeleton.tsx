import { STRINGS } from "@/constants/strings";

import styles from "./NewsFeedSkeleton.module.css";

const SKELETON_ITEMS = ["first", "second", "third"];

export function NewsFeedSkeleton() {
  return (
    <div
      className={styles.list}
      role="status"
    >
      <span className={styles.visuallyHidden}>{STRINGS.newsFeed.loading}</span>
      {SKELETON_ITEMS.map((item) => (
        <div
          key={item}
          className={styles.card}
          aria-hidden="true"
        >
          <div className={styles.heading}>
            <div className={`${styles.block} ${styles.title}`} />
            <div className={`${styles.block} ${styles.author}`} />
          </div>
          <div className={styles.content}>
            <div className={`${styles.block} ${styles.line}`} />
            <div className={`${styles.block} ${styles.line}`} />
            <div className={`${styles.block} ${styles.line} ${styles.lineShort}`} />
          </div>
        </div>
      ))}
    </div>
  );
}

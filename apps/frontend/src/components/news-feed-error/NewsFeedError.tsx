import { STRINGS } from "@/constants/strings";

import styles from "./NewsFeedError.module.css";

export function NewsFeedError() {
  return (
    <div
      className={styles.error}
      role="alert"
    >
      <svg
        className={styles.icon}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <circle
          cx="12"
          cy="12"
          r="9"
        />
        <path d="M12 7.5v5" />
        <path d="M12 16.5h.01" />
      </svg>
      <div className={styles.text}>
        <h2 className={styles.title}>{STRINGS.newsFeed.error.title}</h2>
        <p className={styles.description}>{STRINGS.newsFeed.error.description}</p>
      </div>
    </div>
  );
}

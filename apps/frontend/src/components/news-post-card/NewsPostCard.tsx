import { STRINGS } from "@/constants/strings";
import type { NewsPost } from "@/types/news-post";

import styles from "./NewsPostCard.module.css";

interface NewsPostCardProps {
  newsPost: NewsPost;
}

export function NewsPostCard({ newsPost }: NewsPostCardProps) {
  return (
    <article className={styles.card}>
      <div className={styles.heading}>
        <h2 className={styles.title}>{newsPost.title}</h2>
        <span className={styles.author}>
          {STRINGS.newsPost.authorPrefix}
          {newsPost.author}
        </span>
      </div>
      <p className={styles.content}>{newsPost.content}</p>
    </article>
  );
}

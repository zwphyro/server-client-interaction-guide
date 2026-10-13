import { useEffect, useState } from "react";

import { env } from "@/lib/env";
import type { NewsPost } from "@/types/news-post";

export function useNewsPosts() {
  const [isError, setIsError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [newsPosts, setNewsPosts] = useState<NewsPost[]>([]);

  useEffect(() => {
    const fetchNewsPosts = async () => {
      try {
        const response = await fetch(`${env.nextPublicBackendUrl}/api/v1/news-posts/`);
        const data = await response.json() as NewsPost[];
        setNewsPosts(data);
        setIsLoading(false);
      } catch (error) {
        console.log(error);
        setIsError(true);
      }
    };
    void fetchNewsPosts();
  }, []);

  return {
    isLoading,
    isError,
    newsPosts,
  };
}

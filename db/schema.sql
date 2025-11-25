

CREATE TABLE public.claimed_contracts (
  contract_id uuid NOT NULL,
  user_id uuid NOT NULL,
  claimed_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT claimed_contracts_pkey PRIMARY KEY (contract_id, user_id),
  CONSTRAINT fk_contract FOREIGN KEY (contract_id) REFERENCES public.contracts(contract_id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.profiles(id)
);
CREATE TABLE public.comments (
  comment_id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  post_id uuid NOT NULL,
  parent_comment_id uuid,
  content text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT comments_pkey PRIMARY KEY (comment_id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT fk_post FOREIGN KEY (post_id) REFERENCES public.posts(post_id),
  CONSTRAINT fk_parent_comment FOREIGN KEY (parent_comment_id) REFERENCES public.comments(comment_id)
);
CREATE TABLE public.contracts (
  contract_id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  title text NOT NULL CHECK (char_length(title) > 0),
  description text NOT NULL,
  pay_amount numeric,
  tags ARRAY,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT contracts_pkey PRIMARY KEY (contract_id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT contracts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profiles(id)
);
CREATE TABLE public.direct_messages (
  message_id uuid NOT NULL DEFAULT gen_random_uuid(),
  sender_id uuid NOT NULL,
  receiver_id uuid NOT NULL,
  content text NOT NULL,
  read_at timestamp with time zone,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT direct_messages_pkey PRIMARY KEY (message_id),
  CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES auth.users(id),
  CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES auth.users(id)
);
CREATE TABLE public.friends (
  user_id uuid NOT NULL,
  friend_id uuid NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT friends_pkey PRIMARY KEY (user_id, friend_id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT fk_friend FOREIGN KEY (friend_id) REFERENCES auth.users(id)
);
CREATE TABLE public.posts (
  post_id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  content text NOT NULL CHECK (char_length(content) > 0),
  likes smallint NOT NULL DEFAULT 0,
  dislikes smallint NOT NULL DEFAULT 0,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT posts_pkey PRIMARY KEY (post_id),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES auth.users(id),
  CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profiles(id)
);
CREATE TABLE public.profiles (
  id uuid NOT NULL,
  username text NOT NULL UNIQUE CHECK (char_length(username) >= 3),
  first_name text,
  last_name text,
  tags ARRAY,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT profiles_pkey PRIMARY KEY (id),
  CONSTRAINT fk_auth_users FOREIGN KEY (id) REFERENCES auth.users(id)
);
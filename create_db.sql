create table lists(
    chat_instance varchar(50),
    inline_message_id varchar(50),
    members text,
    primary key (chat_instance, inline_message_id)
);

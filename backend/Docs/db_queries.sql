create table public.alembic_version
(
    version_num varchar(32) not null
        constraint alembic_version_pkc
            primary key
);

alter table public.alembic_version
    owner to "user";

create table public.user_details
(
    id           serial
        primary key,
    name         varchar not null,
    lastname     varchar not null,
    phone_number varchar not null
);

alter table public.user_details
    owner to "user";

create index ix_user_details_id
    on public.user_details (id);

create index ix_user_details_lastname
    on public.user_details (lastname);

create index ix_user_details_name
    on public.user_details (name);

create index ix_user_details_phone_number
    on public.user_details (phone_number);

create table public."user"
(
    id              serial
        primary key,
    email           varchar not null
        unique,
    password        varchar not null,
    user_details_id integer not null
        references public.user_details
);

alter table public."user"
    owner to "user";

create table public.meal
(
    id          serial
        primary key,
    name        varchar not null,
    description varchar not null,
    user_id     integer not null
        references public."user",
    preparation varchar not null
);

alter table public.meal
    owner to "user";

create table public.category
(
    id   serial
        primary key,
    name varchar not null
        unique
);

alter table public.category
    owner to "user";

create table public.meal_category_association
(
    meal_id     integer
        references public.meal,
    category_id integer
        references public.category
);

alter table public.meal_category_association
    owner to "user";

create table public.product
(
    id              serial
        primary key,
    name            varchar           not null
        unique,
    unit_of_measure unitofmeasureenum not null
);

alter table public.product
    owner to "user";

create table public.meal_product_association
(
    meal_id    integer
        references public.meal,
    product_id integer
        references public.product
);

alter table public.meal_product_association
    owner to "user";


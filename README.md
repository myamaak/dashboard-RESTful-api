# week5_API

API server for a simple dashboard service


서버 실행 방법

```bash
python app.py
```

---

# User APIs

**users** 테이블에 존재하는 데이터

|fullname|email|password|id|

|——|——|——|——|

|elice|racer@google.com|234234|1|

|dodo|bird@naver.com|1111|2|

|hatter|mad@elice.co.kr|0000|3|

### SignUp API

서버를 실행한 후 [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register) 에서 POST 요청을 보내는 것으로 signup api가 실행된다. 

예시는 이미 db에 존재하는 유저의 정보이며, 이와 같이 signup api는 fullname, email, password를 입력받는다.

- 입력 예시(다만 해당 예시는 이미 등록된 유저라서 에러가 생긴다.)

```json
{
    "fullname":"elice",
    "email": "racer@google.com",
    "password": "234234"
}
```

 

동작 방식은 다음과 같다.

1. 회원가입 정보가 불충분한 경우 

    위 세가지 정보 중 존재하지 않는 것이 하나라도 있다면 사용자가 채워넣지 않은 정보를 마저 채워넣을 수 있도록 status는 error, message에서는 에러가 발생한 상세 이유를 반환한다. 

    ```json
    {
        "message": "fill in the required information to register",
        "status": "error"
    }
    ```

2. 존재하는 회원 정보일 경우
세가지 정보가 모두 주어졌지만 주어진 email이 유저 데이터베이스에 이미 존재하는 경우, 회원가입을 중단한다. status로는 error, result는 역시 비어있으며 사용자가 이미 존재한다는 사실을 message를 통해 반환한다.

    ```json
    {
        "message": "user already exists",
        "status": "error"
    }
    ```

3. 회원가입이 성공한 경우
데이터베이스의 users 테이블에 사용자 정보가 추가된다. 성공 메세지와 함께 status로 success를 반환한다.

    ```json
    {
        "message": "successfully signed in",
        "result": {
            "email": "racer@google.com",
            "name": "elice"
        },
        "status": "success"
    }
    ```

모든 비밀번호는 암호화되어 저장된다.

### Login API

서버를 실행한 후 [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)에서 POST 요청을 보내는 것으로 signup api가 실행된다.  login api에서는 email, password를 입력받는다.

- 입력 예시

    ```json
    {
    }
    ```

1. 로그인이 실패한 경우
email이 데이터베이스에 존재하지 않거나 password가 유저의 이메일과 일치하지 않는 경우, 둘 중 하나에라도 해당하면 로그인은 실패하고 다음과 같은 메세지를 반환한다.

    ```json
    {
        "message": "invalid user or a wrong password",
        "status": "error"
    }
    ```

2. 로그인이 성공한 경우
전달받은 유저의 정보가 정확하다면 성공 메세지와 함께 result로 로그인 된 유저의 id를 반환한다.

    ```json
    {
        "message": "user is successfully logged in",
        "result": 3,
        "status": "success"
    }
    ```

### Logout API

서버를 실행한 후 [http://127.0.0.1:5000/logout](http://127.0.0.1:5000/logout) 에서 POST 요청을 보내는 것으로 logout api가 실행된다. 아무것도 입력받지 않으며, 현재 세션에 로그인 되어 있는 유저를 로그아웃 시킨다. 실행 결과는 다음과 같다

```json
{
    "message": "user is successfully logged out",
    "status": "success"
}
```

---

# Board APIs

|id|boardname|create_date|user_id|

|——|——|——|——|

|1|cat|2021-02-01 00:07:56|1|

|2|bird||2|

|3|dog||3|

### Read API

서버를 실행한 후 [http://127.0.0.1:5000/board](http://127.0.0.1:5000/board) 에서 GET 요청을 보내는 것으로 read api가 실행된다.  입력값은 필요로 하지 않으며 현재 결과는 다음과 같다.

```json
{
    "message": "printing board list",
    "result": [
        {
            "boardname": "cat",
            "create_date": "2021-02-01 00:07:56",
            "id": 1,
            "user_id": 1
        },
        {
            "boardname": "bird",
            "create_date": "2021-02-01 00:36:39",
            "id": 2,
            "user_id": 2
        },
        {
            "boardname": "dog",
            "create_date": "2021-02-01 00:40:04",
            "id": 3,
            "user_id": 3
        }
    ],
    "status": "success"
}
```

### Create API

서버를 실행한 후 [http://127.0.0.1:5000/board](http://127.0.0.1:5000/board) 에서 POST 요청을 보내는 것으로 create api가 실행된다.  게시판의 이름인 name을 입력받아 새로운 게시판을 생성한다.

- 입력 예시

    ```json
    {
        "name": "board"
    }
    ```

1. 유저가 로그인이 되어있지 않은 경우
로그인 되지 않은 유저가 새로운 게시판을 만들려고 하는 경우 먼저 로그인을 한 후 게시판을 생성해달라는 에러 메세지를 반환하고, 새로운 게시판은 생성하지 않는다. 

    ```json
    {
        "message": "you have to login first to create a board",
        "status": "error"
    }
    ```

2. 게시판 생성 성공
유저가 로그인이 되어있다면 로그인 되어있는 유저를 게시판의 관리자로 설정하고, 입력받은 name을 가지는 새로운 게시판을 생성한다.

    ```json
    {
        "message": "new board is added",
        "result": {
            "boardname": "cat"
        },
        "status": "success"
    }
    ```

### Update API

서버를 실행한 후 [http://127.0.0.1:5000/board](http://127.0.0.1:5000/board) 에서 PUT 요청을 보내는 것으로 update api가 실행된다.  게시판의 id와 바꾸고자 하는 name을 입력받아 해당 id의 게시판 이름을 수정한다.

- 입력 예시

```json
{
    "id":3,
    "name": "dog only"
}
```

1. 유저가 로그인이 되어있지 않은 경우
로그인 되지 않은 유저가 게시판을 수정하려고 하면 에러 메세지를 반환한다.

    ```json
    {
        "message": "you have to login first to change board name",
        "status": "error"
    }
    ```

2. 유저가 수정하고자 하는 게시판을 만든 당사자가 아닐 경우
다른 사람이 만든 게시판을 수정하려고 하는 경우에도 에러메세지가 반환된다.

    ```json
    {
        "message": "the user is not allowed to update current board",
        "status": "error"
    }
    ```

3. 게시판 이름 수정 성공
앞의 두 경우에 해당하지 않는다면 게시판 이름을 성공적으로 수정할 수 있다. 결과는 다음과 같다.

    ```json
    {
        "message": "successfully changed board name",
        "result": {
            "id": "3",
            "name": "dog only"
        },
        "status": "success"
    }
    ```

### Delete API

서버를 실행한 후 [http://127.0.0.1:5000/board](http://127.0.0.1:5000/board) 에서 DELETE 요청을 보내는 것으로 delete api가 실행된다.  게시판의 id를 입력받아 해당 id의 게시판을 삭제한다.

- 입력 예시

```json
{
    "id":4
}
```

1. 유저가 로그인이 되어있지 않은 경우
로그인 되지 않은 유저가 게시판을 삭제하려고 하면 에러 메세지를 반환한다.

    ```json
    {
        "message": "you have to login first to change board name",
        "status": "error"
    }
    ```

2. 유저가 수정하고자 하는 게시판을 만든 당사자가 아닐 경우
다른 사람이 만든 게시판을 삭제하려고 하는 경우에도 에러메세지가 반환된다.

    ```json
    {
        "message": "the user is not allowed to update current board",
        "status": "error"
    }
    ```

3. 게시판 삭제 성공
위 두가지 경우에 해당되지 않는다면 정상적으로 게시판이 삭제된다. 결과는 다음과 같이 반환된다.

    ```json
    {
        "message": "successfully deleted",
        "result": {
            "id": "4"
        },
        "status": "success"
    }
    ```

---

# BoardArticle APIs

### Read API

서버를 실행한 후 [http://127.0.0.1:5000/](http://127.0.0.1:5000/board)board/<board_id> 에서 GET 요청을 보내면 해당하는 board_id의 모든 게시글이 반환된다.

서버를 실행한 후  [http://127.0.0.1:5000](http://127.0.0.1:5000/board)/board/<board_id>/<board_article_id> 에서 GET 요청을 보내면 board_article_id가 일치하는 게시글 하나만 반환된다.

### Create API

서버를 실행한 후 [http://127.0.0.1:5000/](http://127.0.0.1:5000/board)board/<board_id> 에서 POST 요청을 보내는 것으로 create api가 실행된다.  게시글의 제목과 내용을 입력하면 해당하는 board_id의 게시판에 게시글이 생성된다.

- 입력 예시

```json
{
    "title": "sigore jobujong",
    "content": "is cute..."
}
```

- 성공 예시

```json
{
    "message": "successfully posted a new article",
    "result": {
        "title": "sigore jobujong"
    },
    "status": "success"
}
```

다른 사람이 생성한 게시판에서도 게시글을 작성할 수 있으며 작성자 id와 게시글 id 역시 자동으로 db에 저장된다. 

에러 메세지가 반환되는 경우는 다음과 같다.

1. 로그인 된 유저가 아닐 경우

### Update API

서버를 실행한 후 [http://127.0.0.1:5000](http://127.0.0.1:5000/board)/board/<board_id>/<board_article_id> 에서 PUT 요청을 보내는 것으로 update api가 실행된다.  게시글의 제목과 내용을 입력하면 해당하는 board_id의 게시판에서 일치하는 board_article_id의 게시글이 수정된다.

- 입력 예시

```json
{
    "title": "sigore jobujong",
    "content": "is really cute..."
}
```

- 성공 예시

```json
{
    "message": "successfully updated an article",
    "result": {
        "content": "is really cute...",
        "title": "sigore jobujong"
    },
    "status": "success"
}
```

에러 메세지가 반환되는 경우는 다음과 같다.

1. 로그인 된 유저가 아닐 경우
2. 수정하려는 게시글을 본인이 작성하지 않았을 경우

### Delete API

서버를 실행한 후 [http://127.0.0.1:5000](http://127.0.0.1:5000/board)/board/<board_id>/<board_article_id> 에서 DELETE 요청을 보내는 것으로 delete api가 실행된다. url외에는 입력을 필요로 하지 않는다.

- 성공 예시

```json
{
    "message": "successfully deleted",
    "result": {
        "id": "7"
    },
    "status": "success"
}
```

에러 메세지가 반환되는 경우는 다음과 같다.

1. 로그인 된 유저가 아닐 경우
2. 삭제하려는 게시글을 본인이 작성하지 않았을 경우

---

# DashBoard APIs

서버를 실행한 후 [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard) 에서 GET 요청을 보내는 것으로 dashboard api가 실행된다. 각 게시판마다 출력하고자 하는 게시글 갯수 n을 입력값으로 받는다.

- 입력예시

```json
{
    "n":2
}
```

- 출력예시

```json
{
    "result": [
        "meow",
        "cats should",
        "dodo",
        "racoon",
        "welsh corgi",
        "sigore jobujong"
    ],
    "status": "success"
}
```

요청한 게시글 갯수의 크기보다 존재하는 게시글 갯수가 적으면 있는 게시글만 출력된다.
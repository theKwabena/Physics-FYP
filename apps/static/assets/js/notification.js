
    // console.log(user_id)
    const send_notificationSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/notification/'
    );
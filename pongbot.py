def track_ball(ball, paddle, HEIGHT):
    if ball.x_vel < 0: # ball is moving left
        if HEIGHT / 2 >  paddle.y + paddle.height / 2:
            return 'DOWN'
        if HEIGHT / 2 < paddle.y + paddle.height / 2:
            return 'UP'
        if HEIGHT / 2 == paddle.y + paddle.height / 2:
            return 'STAY'
    
    if ball.y >  paddle.y + paddle.height / 2:
        return 'DOWN'
    if ball.y < paddle.y + paddle.height / 2:
        return 'UP'
    if ball.y == paddle.y + paddle.height / 2:
        return 'STAY'

def find_intercept(ball, paddle, HEIGHT):
    intercept = ball.y + ball.y_vel * (paddle.x - ball.x) / ball.x_vel
    return filter_intercept(intercept, HEIGHT)
    
def filter_intercept(intercept, HEIGHT):
    if intercept > 0 and intercept < HEIGHT: # doesn't bounce off the walls anymore -> FINAL STATE
        return intercept
    if intercept < 0: # bounces off the top
        return filter_intercept(-intercept, HEIGHT)
    if intercept > HEIGHT: # bounce off the bottom
        return filter_intercept(HEIGHT * 2 - intercept, HEIGHT)

def predict_ball(ball, paddle, HEIGHT):
    if ball.x_vel < 0: # ball is moving left
        if HEIGHT / 2 >  paddle.y + paddle.height / 2:
            return 'DOWN'
        if HEIGHT / 2 < paddle.y + paddle.height / 2:
            return 'UP'
        if HEIGHT / 2 == paddle.y + paddle.height / 2:
            return 'STAY'

    if ball.x_vel > 0:
        intercept = find_intercept(ball, paddle, HEIGHT)
        if intercept >  paddle.y + paddle.height / 2:
            return 'DOWN'
        if intercept < paddle.y + paddle.height / 2:
            return 'UP'
        if intercept == paddle.y + paddle.height / 2:
            return 'STAY'
        
        

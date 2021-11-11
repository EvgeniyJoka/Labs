def console_and_move():

    while True:
        n = input('Введите желаемое положение двигателя (h - справка) > ')

        if n == 'h':
            print('\nСправка:')
            print('     число - сдвиг двигателя на указанное расстояние (в мм)')
            print('     s - показать текущее положение двигателя')
            print('     z - уствновить двигатель на 0')
            print('     q - выход')
            print('Try in now!\n')

        elif n == 's':
            print(round(steps / k_move), ' мм')

        elif n == 'z':
            stepBackward(abs(steps))
            steps = 0
            print(round(steps / k_move), ' мм')

        elif n == 'q':
            stepBackward(abs(steps))
            exit

        else:
            n = int(n)
            if (n in (0, 100)):
                if n * k_move < steps:
                    
                    stepBackward(abs(n * k_move - steps))
                if n * k_move > steps:
                    stepForward(n * k_move - steps)
                                    

                steps += n * k_move
            else:
                print('Попробуйте снова/n')
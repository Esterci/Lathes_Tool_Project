################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.c 

OBJS += \
./Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.o 

C_DEPS += \
./Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.d 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.o: ../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F103xB -DDEBUG -c -I../Middlewares/Third_Party/FreeRTOS/Source/include -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Drivers/STM32F1xx_HAL_Driver/Inc -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3 -I../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../Drivers/CMSIS/Include -I../Core/Inc -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Drivers/CMSIS/Include -I../Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS -I../Drivers/STM32F1xx_HAL_Driver/Inc -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Middlewares/Third_Party/FreeRTOS/Source/include -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Drivers/CMSIS/Device/ST/STM32F1xx/Include -IC:/Users/MarcosVictor/STM32Cube/Repository/STM32Cube_FW_F1_V1.8.0/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3 -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.d" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"


/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "stream_buffer.h"
#include "cmsis_os2.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
StreamBufferHandle_t xStreamBuffer;
StreamBufferHandle_t zStreamBuffer;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
RTC_HandleTypeDef hrtc;

SPI_HandleTypeDef hspi1;
DMA_HandleTypeDef hdma_spi1_rx;
DMA_HandleTypeDef hdma_spi1_tx;

TIM_HandleTypeDef htim1;

/* Definitions for enviaTask */
osThreadId_t enviaTaskHandle;
const osThreadAttr_t enviaTask_attributes = {
  .name = "enviaTask",
  .priority = (osPriority_t) osPriorityNormal,
  .stack_size = 128 * 4
};
/* Definitions for aquisitaTask */
osThreadId_t aquisitaTaskHandle;
const osThreadAttr_t aquisitaTask_attributes = {
  .name = "aquisitaTask",
  .priority = (osPriority_t) osPriorityHigh,
  .stack_size = 128 * 4
};
/* Definitions for habAQ */
osSemaphoreId_t habAQHandle;
const osSemaphoreAttr_t habAQ_attributes = {
  .name = "habAQ"
};
/* Definitions for habENV */
osSemaphoreId_t habENVHandle;
const osSemaphoreAttr_t habENV_attributes = {
  .name = "habENV"
};
/* USER CODE BEGIN PV */
int i=0, j=0, k=0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_SPI1_Init(void);
static void MX_RTC_Init(void);
static void MX_TIM1_Init(void);
void StartEnviaTask(void *argument);
void StartAquisitaTask(void *argument);

/* USER CODE BEGIN PFP */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin);
void Reset(void);
void Oversampling(void);
void Range(void);
void Converst(void);
void Read(void);
int aquisicao(void);//uint8_t i);
void envia (void);
void vAFunction( void );
void vA_send_Function(  uint8_t to_send[16] );
void vA_receive_Function(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_SPI1_Init();
  MX_RTC_Init();
  MX_TIM1_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_Base_Start_IT(&htim1);
  /* USER CODE END 2 */

  /* Init scheduler */
  osKernelInitialize();

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* Create the semaphores(s) */
  /* creation of habAQ */
  habAQHandle = osSemaphoreNew(1, 1, &habAQ_attributes);

  /* creation of habENV */
  habENVHandle = osSemaphoreNew(1, 1, &habENV_attributes);

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */

  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of enviaTask */
  enviaTaskHandle = osThreadNew(StartEnviaTask, NULL, &enviaTask_attributes);

  /* creation of aquisitaTask */
  aquisitaTaskHandle = osThreadNew(StartAquisitaTask, NULL, &aquisitaTask_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* Start scheduler */
  osKernelStart();
 
  /* We should never get here as control is now taken by the scheduler */
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE|RCC_OSCILLATORTYPE_LSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.LSEState = RCC_LSE_ON;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_RTC;
  PeriphClkInit.RTCClockSelection = RCC_RTCCLKSOURCE_LSE;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief RTC Initialization Function
  * @param None
  * @retval None
  */
static void MX_RTC_Init(void)
{

  /* USER CODE BEGIN RTC_Init 0 */

  /* USER CODE END RTC_Init 0 */

  /* USER CODE BEGIN RTC_Init 1 */

  /* USER CODE END RTC_Init 1 */
  /** Initialize RTC Only 
  */
  hrtc.Instance = RTC;
  hrtc.Init.AsynchPrediv = 127;
  hrtc.Init.OutPut = RTC_OUTPUTSOURCE_SECOND;
  if (HAL_RTC_Init(&hrtc) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN RTC_Init 2 */

  /* USER CODE END RTC_Init 2 */

}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_SLAVE;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi1.Init.NSS = SPI_NSS_HARD_INPUT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_4;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 35;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 1333;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}

/** 
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void) 
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Channel2_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel2_IRQn, 5, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel2_IRQn);
  /* DMA1_Channel3_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel3_IRQn, 5, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel3_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, Cvrst_Pin|Cs_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, Os0_Pin|rst_Pin|ce_Pin|Os1_Pin 
                          |Os2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : PC13 */
  GPIO_InitStruct.Pin = GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pin : ext_nss_Pin */
  GPIO_InitStruct.Pin = ext_nss_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(ext_nss_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : Frsdt_Pin */
  GPIO_InitStruct.Pin = Frsdt_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(Frsdt_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : Cvrst_Pin Cs_Pin ce_Pin */
  GPIO_InitStruct.Pin = Cvrst_Pin|Cs_Pin|ce_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : Busy_Pin */
  GPIO_InitStruct.Pin = Busy_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(Busy_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : db0_Pin db1_Pin db2_Pin db10_Pin 
                           db11_Pin db12_Pin db13_Pin db14_Pin 
                           db15_Pin db3_Pin db4_Pin db5_Pin 
                           db6_Pin db7_Pin db8_Pin db9_Pin */
  GPIO_InitStruct.Pin = db0_Pin|db1_Pin|db2_Pin|db10_Pin 
                          |db11_Pin|db12_Pin|db13_Pin|db14_Pin 
                          |db15_Pin|db3_Pin|db4_Pin|db5_Pin 
                          |db6_Pin|db7_Pin|db8_Pin|db9_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : Os0_Pin rst_Pin Os1_Pin Os2_Pin */
  GPIO_InitStruct.Pin = Os0_Pin|rst_Pin|Os1_Pin|Os2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI3_IRQn, 5, 0);
  HAL_NVIC_EnableIRQ(EXTI3_IRQn);

}

/* USER CODE BEGIN 4 */
void Reset(void)
{
	HAL_GPIO_WritePin(GPIOA, rst_Pin, 1);
	HAL_GPIO_WritePin(GPIOA, rst_Pin, 0);

}
void Oversampling(void)
{
	HAL_GPIO_WritePin(GPIOA, Os0_Pin, 0);
	HAL_GPIO_WritePin(GPIOA, Os1_Pin, 0);
	HAL_GPIO_WritePin(GPIOA, Os2_Pin, 0);

}
void Range(void)
{
	//HAL_GPIO_WritePin(GPIOA, range_Pin, 1);

}
void Converst(void)
{
	 HAL_GPIO_WritePin(GPIOA, Cvrst_Pin, 0);
	 HAL_GPIO_WritePin(GPIOA, Cvrst_Pin, 1);
}

 void Read(void)
{

	 	size_t xBytesSent;
	 	size_t zBytesSent;
	 	const TickType_t x100ms = pdMS_TO_TICKS( 100 );
	 	BaseType_t xEmpty;
	 	BaseType_t zEmpty;
	 	uint16_t valor;
	 	static unsigned char valor2;
	 	static unsigned char valor3;
	 	static unsigned char canais[400];



	 		for (i=0+k; i<k+16;)
	 			{
	 				HAL_GPIO_WritePin(GPIOA, Cs_Pin, 0);
	 				HAL_GPIO_WritePin(GPIOA, ce_Pin, 1);

	 				valor = GPIOB->IDR;
	 				valor2 = (valor & 255);
	 				valor3 = ((valor>>8) & 255);
	 				canais[i]= valor3;
	 				canais[i+1]= valor2;

	 			//if (HAL_GPIO_ReadPin(GPIOA, Frsdt_Pin)==1)
	 			////{
	 				//i=0;
	 			//}


	 				i=i+2;
	 				HAL_GPIO_WritePin(GPIOA, Cs_Pin, 1);
	 				HAL_GPIO_WritePin(GPIOA, ce_Pin, 0);

	 			}
	 		j++;
	 		k=k+16;



	 		if(j>=24)
	 		 	{
	 			 __HAL_TIM_DISABLE_IT(&htim1, TIM_IT_BREAK);
	 			  xEmpty = xStreamBufferIsEmpty(xStreamBuffer );
	 			  if (xEmpty==pdTRUE)
	 			  {
	 				 xBytesSent = xStreamBufferSend( xStreamBuffer, (void *)canais, 400, x100ms );

	 			   if (xBytesSent == sizeof( canais ))
	 			    {
	 				  osSemaphoreRelease (habENVHandle);
	 			    }
	 			  }
	 			 else if (xEmpty==pdFALSE)
	 			  {
	 			   zEmpty = xStreamBufferIsEmpty(zStreamBuffer );
	 			   if (zEmpty==pdTRUE)
	 			    {
	 				 zBytesSent = xStreamBufferSend( zStreamBuffer, (void *)canais, 400, x100ms );

	 				  if (zBytesSent == sizeof( canais ))
	 				   {
	 					 osSemaphoreRelease (habENVHandle);
	 				   }
	 		 	    }
	 	          }
	 		 	}


}




/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	if (GPIO_Pin == Busy_Pin)

	{
	 osSemaphoreRelease (habAQHandle);
 	}

}
void vAFunction( void )
{
	//StreamBufferHandle_t xStreamBuffers;
	const size_t xStreamBufferSizeBytes = 2656, xTriggerLevel = 2656;

    /* Create a stream buffer that can hold 100 bytes.  The memory used to hold
    both the stream buffer structure and the data in the stream buffer is
    allocated dynamically. */
    xStreamBuffer = xStreamBufferCreate( xStreamBufferSizeBytes, xTriggerLevel );
    zStreamBuffer = xStreamBufferCreate( xStreamBufferSizeBytes, xTriggerLevel );

    //if( xStreamBuffer == NULL )
    //{
        /* There was not enough heap memory space available to create the
        stream buffer. */
   // }
   // else
    //{
        /* The stream buffer was created successfully and can now be used. */
   // }
}


/* USER CODE END 4 */

/* USER CODE BEGIN Header_StartEnviaTask */
/**
  * @brief  Function implementing the enviaTask thread.
  * @param  argument: Not used 
  * @retval None
  */
/* USER CODE END Header_StartEnviaTask */
void StartEnviaTask(void *argument)
{
  /* USER CODE BEGIN 5 */
  vAFunction();
  static unsigned char ucRxData[400];
  size_t xReceivedBytes;
  size_t zReceivedBytes;
  BaseType_t xFull;
  BaseType_t zFull;
  const TickType_t xBlockTime = pdMS_TO_TICKS( 20 );
	  /* Infinite loop */
  for(;;)
  {
	osSemaphoreAcquire (habENVHandle, osWaitForever);
	i=0, j=0, k=0;
	xFull = xStreamBufferIsFull( xStreamBuffer );
	if (xFull==pdTRUE)
		{
		  xReceivedBytes = xStreamBufferReceive( xStreamBuffer, (void *)ucRxData, 400, xBlockTime );
		  if( xReceivedBytes == sizeof( ucRxData ) )
			{
			 HAL_SPI_Transmit_DMA(&hspi1, ucRxData, 400);
			 xStreamBufferReset(zStreamBuffer);
			 __HAL_TIM_ENABLE_IT(&htim1, TIM_IT_BREAK);
			}
		 }
	else if (xFull==pdFALSE)
		{
		  zFull = xStreamBufferIsFull( zStreamBuffer );
		  if (zFull==pdTRUE)
		  	 {
			  zReceivedBytes = xStreamBufferReceive( zStreamBuffer, (void *)ucRxData, 400, xBlockTime );
			  if( zReceivedBytes == sizeof( ucRxData ) )
		  		 {
				  HAL_SPI_Transmit_DMA(&hspi1, ucRxData, 400);
				  xStreamBufferReset(xStreamBuffer);
		  			__HAL_TIM_ENABLE_IT(&htim1, TIM_IT_BREAK);
		  		 }
		  	  }
		 }
  }
}


  /* USER CODE END 5 */ 


/* USER CODE BEGIN Header_StartAquisitaTask */
/**
* @brief Function implementing the aquisitaTask thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartAquisitaTask */
void StartAquisitaTask(void *argument)
{
  /* USER CODE BEGIN StartAquisitaTask */
	vAFunction();
  /* Infinite loop */
  for(;;)
  {
	  //Converst();
	  osSemaphoreAcquire (habAQHandle, osWaitForever );
	  Read();
	  osDelay(0);

  }
  /* USER CODE END StartAquisitaTask */
}

 /**
  * @brief  Period elapsed callback in non blocking mode
  * @note   This function is called  when TIM2 interrupt took place, inside
  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
  * a global variable "uwTick" used as application time base.
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* USER CODE BEGIN Callback 0 */
  if (htim->Instance == TIM1) {

	  {
		  Converst();
	  }
  }

  /* USER CODE END Callback 0 */
  if (htim->Instance == TIM2) {
    HAL_IncTick();
  }
  /* USER CODE BEGIN Callback 1 */

  /* USER CODE END Callback 1 */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/

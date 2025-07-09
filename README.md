# Smart-Clothing-Sorting-System

### 本项目用于驱动基于串口的modbus 协议控制继电器，以之驱动电机工作，使用opencv 和yolo进行 图像识别，将识别结果和电机对应驱动器绑定起来，如此能够实现自动化分拣衣物

## 流程图


```mermaid
      flowchart TB
        subgraph 从左到右
          direction LR
          声明图像类型1 --> 声明排列方向1 --> 声明图像内容1
        end
        subgraph 从右到左
          direction RL
          声明图像类型2 --> 声明排列方向2 --> 声明图像内容2
        end
        subgraph 上下分明
          direction LR
          subgraph 从上到下
            direction TB
            声明图像类型3 --> 声明排列方向3 --> 声明图像内容3
          end
          subgraph 从下到上
            direction BT
            声明图像类型4 --> 声明排列方向4 --> 声明图像内容4
          end
          从上到下 --> 从下到上
        end
        从左到右 --> 从右到左 --> 上下分明
        ```

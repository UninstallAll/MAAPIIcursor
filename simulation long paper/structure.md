abstract
ccs concepts

Introduction

concept

technical description

conclusion

biographies


ackownledgements

references

可能的标题：
Aligning Medium and Meaning: The Technical Genealogy of 'Prosomoíosi (Simulation)'

对齐媒介，重写图像：AI 影像实践的批判框架

技术模拟与媒介对齐：生成时代影像方法论

从模拟到媒介对齐：重塑视觉记忆的技术路径

由模拟驱动的媒介对齐：后数字影像的新范式

introduction
过去十年，生成式人工智能（generative AI）对视听媒介的冲击已从科研实验室迅速扩散至电影工业核心流程。2024 年奥斯卡主办方首次明确允许含有 AI 生成镜头的作品参评——这一象征性举措不仅折射出好莱坞对技术范式转移的认可，也宣告了传统电影生产标准的松动。同年，纽约与洛杉矶的 Runway AI Film Festival 以及巴塞罗那雨电影节（RAIN Film Fest）等活动相继举办，预示着 AI 影像创作正从边缘艺术实践走向规模化生态；2025 年首届亚洲 AI 电影节（HKUST AI Film Festival）的启动，则进一步印证了这一全球趋势的地理扩散与文化多样化。
技术层面，生成式模型在脚本撰写、分镜设计、图像合成乃至长序列视频生成的突破为创作者打开了前所未有的实时迭代空间。文本到视频模型（text-to-video）——如 Runway Gen-2、OpenAI 的 Sora、Google 的 Veo 等——借助大规模时空扩散框架，实现了可控、高清且叙事连贯的影像输出；与此同时，Stable Diffusion、Flux、Midjourney 等文本到图像模型（text-to-image）和大型语言模型（LLM）在剧本开发与世界观设定中的协同作用，正在重塑传统的前期筹备流程。研究者指出，AI 生成工具不仅提高了制作效率，更在审美层面引入了“机器视觉”的文化语法，使创作与观众感知同步迭代。

技术突进令人兴奋，却也暴露出一个被忽视的核心矛盾：当艺术家在创作中拥抱全新的媒介，却继续沿用旧有的观念框架（或反之，以新概念驱动旧媒介），媒介与理念之间便产生错位。结果往往是——
1.新技术仅被当作“加速器”，无法真正参与作品立意；
2.概念被迫让位于工具可实现性的既定范式，呈现出“演示式”或“炫技式”的浅层效果；
3.观众感知到的是“技术惊奇”而非作品主旨，进而削弱对艺术表达本身的关注。

本文正是针对这一“媒介／概念错位”现象展开讨论，并以影像作品《Prosomoíosi (Simulation)》为核心案例。该作品以“模拟”作为切入点，通过对模拟技术、历史与文化语义的系列考察，逐步提出并阐发“媒介对齐”（medium alignment）概念：即在创作过程中主动对准（re-align）作品的思想诉求与所采用媒介的运算逻辑，使技术流程成为概念表达的可感知部分，而非被掩藏的后台。作品所采用的技术架构——在 TouchDesigner 内部调用 StreamDiffusion 进行图像实时生成，并结合动态参数曲线与 ComfyUI Flux 的分区放大——本身即是这一理念的具身实践：扩散过程被公开展示并纳入叙事，令观众得以直接感知算法如何塑造影像。本文将说明：唯有在“媒介对齐”的前提下，生成式影像才能超越工具主义与炫技倾向，成为重新协商记忆、历史与主体性的动态场域。







技术部分：

技术描述（约半页）

本作品的实时生成链路由「素材准备→扩散生成→高分辨率放大→后期处理」四个阶段组成，每一阶段均经过针对演性的优化。

1. 素材准备  
   • 源素材分为两类：①公共领域旧影片／纪录片片段；③实机演示录制输出的游戏片段。所有素材在primiere pro 中统一转码为24 fps、h.264编码，为后续生成做准备。并且在同一个sequence内完成前期的剪辑
   • 在使用4090显卡作为关键硬件平台的前提下，为给扩散模型留出演算时间，素材首先在primiere pro内被减速至4或14fps，既原速率的0.2倍或0.5倍（具体取决于后续所选模型的推理速度）。等待实时通过串流推送软件，例如NDI或spout等软件（本作使用了NDI），推送至touchdesigner进行试试扩散生成。

2. 实时扩散生成（TouchDesigner + StreamDiffusion 插件）  
   • 硬件：AMD Ryzen 9 7950X / NVIDIA RTX 4090 (24 GB VRAM)。  
   • 在 TouchDesigner 中加载由dotsimulate 开发的的 StreamDiffusion 节点，在配置好项目依赖环境后，对全部视频帧做图像到图像（img2img）扩散。根据艺术效果需要动态切换 Stable Diffusion XL、Stable Diffusion 1.5 等模型及其 LoRA。
   • 在 TouchDesigner 中使用 Animation COMP 的曲线表将 StreamDiffusion 的 Prompt、CFG Scale、Steps、Denoise 等参数绑定到关键帧曲线上，可通过曲线精细控制所有生成参数；表演者可预设或实时编辑曲线，以动态塑造叙事节奏，获得更加顺滑和连贯的生成效果。
    • 此外，工作流程在 TouchDesigner 中集成了 ControlNet 的 HED（Holistically-Nested Edge Detection）分支；通过对边缘强度权重的参数化调节，进一步约束扩散过程对场景几何轮廓与空间定位的收敛性。

   遇到的问题，节点出错，有残影，不定时出现

3. 高分辨率放大（ComfyUI Flux Work-flow）  
   在本Flux图像高清生成工作流中，图像的前处理与区域性重建构成了流程的核心基础。整体设计旨在在保证生成质量的前提下，适应不同显存环境，提升大图处理能力，并增强生成图像的细节表达力。

    首先，图像通过 LoadImage 节点被导入系统，并由 ImageResizeKJ 节点统一调整至指定的标准尺寸（如1024×1024）。该处理确保图像格式与后续模块兼容，并可通过插值算法控制缩放方式。随后，UpscaleModelLoader 节点加载超分辨率模型（如 "4x_NMKD-Siax_200k"），并在 ImageUpscaleWithModel 中实现对图像的真实四倍放大。此步不仅提升分辨率，也为后续的生成与细化奠定了高维基础，从而增强了整体的纹理表达与边缘锐度。

    在图像放大完成后，为进一步缓解高分辨率带来的显存压力，并支持多tile并行生成，系统引入了TTP（Tile-to-Patch）切片机制。具体而言，TTP_Tile_image_size 节点依据图像尺寸与设定的网格数，自动计算适当的 tile 宽高参数；TTP_Image_Tile_Batch 节点则据此将整图划分为多个小块，并输出 tile 图像批次、位置信息、原图尺寸及网格结构。每个 tile 随后被独立处理并编码至潜空间，以适配Flux模型的生成流程。

    在图像生成完毕后，系统使用 TTP_Image_Assy 节点，根据 tile 的位置与原图布局参数，将各子图进行空间复原，最终重构出一张具备整体结构连续性且细节丰富的完整图像。该机制有效平衡了显存与分辨率之间的矛盾，实现了局部生成与全局一致性的统一。

4. 输出与展示 
   • 将 Flux 工作流放大后的 4K 图像序列（4096×4096 PNG）整体导入 Adobe After Effects，保持 24 fps 时间基准。后期阶段利用 Lumetri Color、Camera Lens Blur、Optical Flares 等插件完成色彩校正、景深模拟与光影合成。  
   • 按放映规范（DCI 4K 4096×2160／24 fps／Rec. 709 Gamma 2.4）渲染母版后，使用 Topaz Video AI 进行最终帧插值（Chronos 2× 或 4×）与锐化（Artemis High Quality），输出既满足影院 DCP 也可用于展厅循环播放的成片。


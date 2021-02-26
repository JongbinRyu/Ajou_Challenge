# **제 1회 아주훌륭한 딥러닝 챌린지**

**대회목표**: 한정된 파라미터를 이용해서 Cifar-100의 영상 인식 성능을 높여라!!

1. **세부 프로토콜**

   데이터셋: Cifar-100 
   
   네트워크 파라미터: weight의 숫자가 300K 이하인 딥러닝 모델 

   아키텍쳐: 자유

   학습알고리즘: 자유

   딥러닝 프레임워크: PyTorch 권장, TensorFlow등 다른 프레임워크도 사용 가능

   외부데이터: 사용하면 안됨

2. **순위산정:** Cifar-100 validation set의 Top-1 Accuracy 3번 평균 (random으로 weight를 초기화 후 3번 학습)

3. **팀 구성**: 기본 1인 1팀, 중간 1차 발표 이후 최대 2인까지 팀 구성 가능

4. **대회진행**

   |     날짜      |      일정       |
   | :-----------: | :-------------: |
   |     시작      | 2021년 1월 11일 |
   | 중간 1차 발표 | 2021년 2월 1일  |
   | 중간 2차 발표 | 2021년 2월 22일 |
   | 최종결과 발표 | 2021년 3월 8일  |

5. **최종 결과 산출 방법:** 2021년 2월 22일의 Accuracy의 20% + 2021년 3월 8일의 Accuracy의 80%


## 퍼블릭 랭킹

  
- 중간 점수 집계(2021-02-22 18:08:59.772858+09:00): Total Score가 업데이트 되었습니다.  
 - 다음 업데이트 일정은 최종 점수 집계(2021-03-08) 입니다.
  
**현재 랭킹 1위는 seungmin 입니다. 평균 accuracy는 70.0% 입니다.**
|Ranking|Name|Penalty|Accuracy(%)|Last Submission|Total Submission Count|Total Score(%)|
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|1|seungmin|0|78.28|2021-02-17 19:06:20.632842+09:00|5|15.656|
|2|hankyul|0|77.27|2021-02-07 09:49:48.202083+09:00|4|15.454|
|3|jihoon|0|75.93|2021-02-16 18:52:03.769036+09:00|17|15.186|
|4|kideok|0|75.52|2021-02-03 17:24:06.404169+09:00|3|15.104|
|5|dohyun|0|70.78|2021-02-22 02:13:41.997080+09:00|1|14.156|
|6|changyeob|0|67.81|2021-01-26 12:16:05.983074+09:00|1|13.562|
|7|juhyun|0|67.4|2021-02-22 09:22:21.363536+09:00|1|13.48|
|8|dongwook|0|63.36|2021-01-18 13:10:59.504522+09:00|2|12.672|
|9|sanghyun|0|62.63|2021-02-16 17:27:57.559770+09:00|4|12.526|
|10|yongha|0|61.02|2021-02-22 17:00:47.463773+09:00|10|12.204|


**정확도는 소숫점 5자리 까지 출력됩니다.**
**Time zone is seoul,korea (UTC+9:00)**
## 퍼블릭 랭킹 제출 방법

본인이름의 폴더 안에 테스트 데이터 셋을 예측한 결과값을 제출 하면 됨. `1.txt`, `2.txt`, `3.txt` 파일들을 읽고 합쳐서 평균 accuracy를 구합니다.

## submission file 추출한 방법 

answer.txt 파일은 다음과 같은 방법으로 추출했습니다. 착오 없길 바랍니다.

```python
import tensorflow as tf
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar100.load_data(
    label_mode='fine'
)
np.savetxt('ans.txt', y_test, fmt='%i')
```




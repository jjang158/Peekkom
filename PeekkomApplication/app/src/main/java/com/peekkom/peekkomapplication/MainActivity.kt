package com.peekkom.peekkomapplication

import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.google.firebase.messaging.FirebaseMessaging
import com.peekkom.peekkomapplication.ui.theme.PeekkomApplicationTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            PeekkomApplicationTheme {
                MainScreen() {}
            }
        }

        // FCM 토큰 로그 출력
        FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
            if (!task.isSuccessful) {
                Log.w("FCM", "Fetching FCM registration token failed", task.exception)
                return@addOnCompleteListener
            }

            val token = task.result
            Log.d("FCM", "FCM Token: $token")
        }
    }
}

@Composable
fun MainScreen() {
    var selectedTab by remember { mutableStateOf("수액") }

    Scaffold { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            // 탭 버튼들
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                listOf("수액", "낙상", "환자", "설정").forEach { tab ->
                    Button(
                        onClick = { selectedTab = tab },
                        colors = if (selectedTab == tab)
                            ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                        else
                            ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(text = tab)
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            // 선택된 탭 내용 표시
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.TopCenter
            ) {
                when (selectedTab) {
                    "수액" -> {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("🧪 수액 모니터링 화면입니다.", fontSize = 20.sp)
                            Spacer(modifier = Modifier.height(16.dp))

                            Image(
                                painter = painterResource(R.drawable.iv_fluid),
                                contentDescription = "수액 이미지",
                                modifier = Modifier.size(200.dp),
                                contentScale = ContentScale.Fit
                            )
                        }
                    }

                    "낙상" -> {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("⚠️ 낙상 알림 화면입니다.", fontSize = 20.sp)
                            Spacer(modifier = Modifier.height(16.dp))

                            Image(
                                painter = painterResource(R.drawable.iv_fall),
                                contentDescription = "낙상 이미지",
                                modifier = Modifier.size(200.dp),
                                contentScale = ContentScale.Fit
                            )
                        }
                    }

                    "환자" -> {
                        Column(horizontalAlignment = Alignment.Start) {
                            Text("📋 환자 목록 화면입니다.", fontSize = 20.sp)
                            Spacer(modifier = Modifier.height(16.dp))

                            val patients = listOf(
                                "🧑 김철수 | 70세 | 입원중",
                                "👩 이영희 | 58세 | 퇴원예정",
                                "🧑 정지훈 | 34세 | 수술대기",
                                "👩 박민정 | 45세 | 외래진료",
                                "🧑 최강민 | 29세 | 정밀검사"
                            )

                            patients.forEach { patient ->
                                Text(
                                    text = patient,
                                    fontSize = 16.sp,
                                    modifier = Modifier.padding(vertical = 4.dp)
                                )
                            }
                        }
                    }

                    "설정" -> {
                        Column(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalAlignment = Alignment.Start
                        ) {
                            Text("🔧 설정 화면입니다.", fontSize = 20.sp)
                            Spacer(modifier = Modifier.height(16.dp))

                            val settings = listOf(
                                "👤 계정 관리",
                                "🔔 알림 설정",
                                "🌙 다크 모드",
                                "📱 앱 버전 정보",
                                "📞 고객센터 / 문의"
                            )

                            settings.forEach { item ->
                                Text(
                                    text = item,
                                    fontSize = 16.sp,
                                    modifier = Modifier.padding(vertical = 4.dp)
                                )
                            }
                        }
                    }
                }
            }
        } // <-- Column 끝
    } // <-- Scaffold 끝
}


@Preview(showBackground = true)
@Composable
fun MainPreview() {
    PeekkomApplicationTheme {
        MainScreen() {}
    }
}

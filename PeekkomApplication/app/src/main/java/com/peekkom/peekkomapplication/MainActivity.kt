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
                Surface(modifier = Modifier.fillMaxSize()) {
                    IVStatusScreen()
                }
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
fun IVStatusScreen() {
    var percentage by remember { mutableStateOf(50) } // 잔여 수액 % 상태
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "\uD83D\uDCA7 수액 상태 확인",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "잔여 수액: $percentage%",
            style = MaterialTheme.typography.bodyLarge
        )

        Spacer(modifier = Modifier.height(32.dp))

        Button(
            onClick = {
                Toast.makeText(context, "테스트 버튼 클릭됨", Toast.LENGTH_SHORT).show()
                percentage = (10..90).random() // 임의 수치 변경
            }
        ) {
            Text("테스트 알림 보기")
        }
    }
}

@Preview(showBackground = true)
@Composable
fun IVStatusScreenPreview() {
    PeekkomApplicationTheme {
        IVStatusScreen()
    }
}

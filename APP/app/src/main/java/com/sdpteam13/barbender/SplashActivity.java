package com.sdpteam13.barbender;

import android.content.Intent;
import android.os.CountDownTimer;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class SplashActivity extends AppCompatActivity {

    @Override
    public void onBackPressed() {
        //close the app as finish() is not effective here due to background counter to intent
        android.os.Process.killProcess(android.os.Process.myPid());
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        // 3 second timeout of splash screen
        new CountDownTimer(3000, 1000) {

            public void onTick(long millisUntilFinished) {}

            public void onFinish() {
                finish(); // finish the activity
                startActivity(new Intent(SplashActivity.this, BarlistActivity.class));
            }
        }.start();
    }
}
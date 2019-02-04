package com.sdpteam13.barbender;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class BarlistActivity extends AppCompatActivity implements View.OnClickListener{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_barlist);
        findViewById(R.id.appleton).setOnClickListener(this);
        findViewById(R.id.peartree).setOnClickListener(this);
        findViewById(R.id.forum).setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        // clickable areas of UI layout
        switch (v.getId()){
            case R.id.appleton:
                startActivity(new Intent(this, SeatActivity.class));
                break;

            case R.id.peartree:
                startActivity(new Intent(this, SeatActivity.class));
                break;

            case R.id.forum:
                startActivity(new Intent(this, SeatActivity.class));
                break;
        }
    }
}
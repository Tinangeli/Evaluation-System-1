<?php

use App\Http\Controllers\EvaluationController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('app/student-evaluation-form', App\Filament\App\Pages\StudentEvaluationForm::class)
    ->name('filament.app.pages.student-evaluation-form')
    ->middleware(['auth']);

Route::get('/fetch-summary', [EvaluationController::class, 'getAISummary']);


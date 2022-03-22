import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchTransactionsPageComponent } from './search-transactions-page.component';

describe('SearchTransactionsPageComponent', () => {
  let component: SearchTransactionsPageComponent;
  let fixture: ComponentFixture<SearchTransactionsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchTransactionsPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchTransactionsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
